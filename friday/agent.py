from __future__ import annotations

import json
from typing import Any

from openai import APIConnectionError, APIError, OpenAI, RateLimitError

from friday.audit import AuditLogger
from friday.config import config
from friday.memory import ConversationMemory
from friday.permissions import PermissionError, PermissionManager
from friday.scheduler import SchedulerManager
from friday.tool_context import ToolContext
from friday.tools import build_registry
from friday.voice import VoiceInterface


class AssistantAgent:
    """Tool-using OpenAI assistant with permissions, memory, and scheduling."""

    def __init__(self) -> None:
        self.config = config
        self.client = OpenAI(api_key=config.openai_api_key) if config.openai_api_key else None
        self.memory = ConversationMemory(max_messages=config.memory_window)
        self.permissions = PermissionManager(config=config)
        self.audit = AuditLogger(config.action_log_path)
        self.voice = VoiceInterface()
        if config.voice_output_enabled:
            self.voice.enable_output(True)

        self.registry = build_registry()
        self.scheduler = SchedulerManager(config.data_dir, poll_interval=config.scheduler_poll_interval)
        self.context = ToolContext(
            config=self.config,
            permissions=self.permissions,
            audit=self.audit,
            memory=self.memory,
            scheduler=self.scheduler,
            voice=self.voice,
            registry=self.registry,
            client=self.client,
        )
        self.scheduler.set_runner(self.run_saved_automation)
        self.scheduler.start()
        self.max_tool_rounds = config.max_tool_rounds

    @property
    def conversation_history(self) -> list[dict[str, str]]:
        return self.memory.messages

    def reset_memory(self) -> None:
        self.memory.clear()

    def list_tools(self) -> list[str]:
        return [tool.name for tool in self.registry.all()]

    def list_automations(self) -> list[dict[str, Any]]:
        return self.scheduler.list_automations()

    def list_schedules(self) -> list[dict[str, Any]]:
        return self.scheduler.list_schedules()

    def set_voice_output(self, enabled: bool) -> str:
        return self.voice.enable_output(enabled)

    def process_command(self, user_input: str) -> dict[str, Any]:
        if not self.client:
            message = self._offline_response(user_input)
            return {"action": "chat", "parameters": {"response": message}, "reasoning": "offline"}

        try:
            reply = self._run_agentic_turn(user_input)
        except (RateLimitError, APIConnectionError, APIError) as exc:
            reply = f"OpenAI request failed: {exc}"
        except Exception as exc:
            reply = f"I hit an unexpected error: {exc}"

        self.voice.speak(reply)
        return {"action": "chat", "parameters": {"response": reply}, "reasoning": "agent"}

    def run_saved_automation(self, name: str) -> dict[str, Any]:
        automation = self.scheduler.get_automation(name)
        if not automation:
            return {"ok": False, "message": f"Automation '{name}' was not found."}

        steps = automation.get("steps", [])
        step_results = []
        for index, step in enumerate(steps, start=1):
            tool_name = step["tool_name"]
            arguments = step.get("arguments", {})
            try:
                result = self._execute_tool(tool_name, arguments)
            except Exception as exc:
                return {
                    "ok": False,
                    "message": f"Automation '{name}' failed at step {index}: {exc}",
                    "step_results": step_results,
                }

            step_results.append({"step": index, "tool_name": tool_name, "result": result})
            if not result.get("ok", False):
                return {
                    "ok": False,
                    "message": f"Automation '{name}' stopped at step {index}.",
                    "step_results": step_results,
                }

        return {
            "ok": True,
            "message": f"Automation '{name}' completed successfully.",
            "step_results": step_results,
        }

    def _run_agentic_turn(self, user_input: str) -> str:
        input_items: list[Any] = self.memory.to_openai_input()
        input_items.append({"role": "user", "content": user_input})

        for _ in range(self.max_tool_rounds):
            response = self.client.responses.create(
                model=self.config.openai_model,
                instructions=self.config.system_prompt,
                input=input_items,
                tools=self.registry.schemas(),
            )

            tool_calls = [item for item in response.output if getattr(item, "type", "") == "function_call"]
            if not tool_calls:
                text = (response.output_text or "").strip()
                if not text:
                    text = "I completed the request, but I did not receive any final text from the model."
                self.memory.add("user", user_input)
                self.memory.add("assistant", text)
                return text

            input_items.extend(self._serialize_output_items(response.output))

            for tool_call in tool_calls:
                try:
                    arguments = json.loads(tool_call.arguments or "{}")
                except json.JSONDecodeError as exc:
                    result = self.context.json_result(
                        ok=False,
                        message=f"Tool arguments for {tool_call.name} were invalid JSON: {exc}",
                    )
                else:
                    result = self._execute_tool(tool_call.name, arguments)

                input_items.append(
                    {
                        "type": "function_call_output",
                        "call_id": tool_call.call_id,
                        "output": self.context.serialize_tool_output(result),
                    }
                )

        return "I stopped after reaching the tool safety limit for this request."

    def _execute_tool(self, tool_name: str, arguments: dict[str, Any]) -> dict[str, Any]:
        if not self.registry.has(tool_name):
            result = self.context.json_result(ok=False, message=f"Unknown tool '{tool_name}'.")
            self.audit.log(event="tool_result", payload={"tool": tool_name, "result": result})
            return result

        spec = self.registry.get(tool_name)
        summary = self._build_confirmation_summary(arguments)

        try:
            if spec.requires_confirmation:
                self.permissions.confirm(tool_name, summary)

            self.audit.log(event="tool_request", payload={"tool": tool_name, "arguments": arguments})
            result = spec.handler(self.context, **arguments)
        except PermissionError as exc:
            result = self.context.json_result(ok=False, message=str(exc))
        except Exception as exc:
            result = self.context.json_result(ok=False, message=f"{tool_name} failed: {exc}")

        self.audit.log(event="tool_result", payload={"tool": tool_name, "result": result})
        return result

    @staticmethod
    def _build_confirmation_summary(arguments: dict[str, Any]) -> str:
        if not arguments:
            return "No arguments supplied"
        preview = ", ".join(f"{key}={value}" for key, value in list(arguments.items())[:3])
        return preview[:240]

    @staticmethod
    def _serialize_output_items(items: list[Any]) -> list[Any]:
        serialized = []
        for item in items:
            if hasattr(item, "model_dump"):
                serialized.append(item.model_dump(exclude_none=True))
            else:
                serialized.append(item)
        return serialized

    def _offline_response(self, user_input: str) -> str:
        lowered = user_input.lower().strip()
        if "time" in lowered or "date" in lowered:
            return self.registry.get("get_current_time").handler(self.context)["message"]
        if lowered in {"tools", "list tools"}:
            return "Available tools: " + ", ".join(self.list_tools())
        return (
            "OpenAI API key is not configured, so the agent cannot plan multi-step actions yet. "
            "Add OPENAI_API_KEY to .env to enable tool calling."
        )


assistant_agent = AssistantAgent()
