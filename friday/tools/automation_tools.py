from __future__ import annotations

from friday.tool_registry import ToolRegistry


def register(registry: ToolRegistry) -> None:
    @registry.register(
        name="save_automation",
        description="Save a reusable automation as a sequence of tool calls.",
        parameters={
            "type": "object",
            "properties": {
                "name": {"type": "string", "description": "Automation name"},
                "description": {"type": "string", "description": "Short human description"},
                "steps": {
                    "type": "array",
                    "description": "Ordered tool calls",
                    "items": {
                        "type": "object",
                        "properties": {
                            "tool_name": {"type": "string"},
                            "arguments": {"type": "object"},
                        },
                        "required": ["tool_name", "arguments"],
                        "additionalProperties": False,
                    },
                },
            },
            "required": ["name", "steps"],
            "additionalProperties": False,
        },
        requires_confirmation=True,
        allow_in_schedule=False,
    )
    def save_automation(context, name: str, steps: list[dict], description: str = "") -> dict:
        _validate_steps(context, steps)
        saved = context.scheduler.save_automation(name, description, steps)
        return context.json_result(ok=True, message=f"Saved automation '{name}'.", automation=saved)

    @registry.register(
        name="run_automation",
        description="Run a saved automation by name.",
        parameters={
            "type": "object",
            "properties": {"name": {"type": "string", "description": "Automation name"}},
            "required": ["name"],
            "additionalProperties": False,
        },
        requires_confirmation=True,
        allow_in_schedule=False,
    )
    def run_automation(context, name: str) -> dict:
        result = context.scheduler.run_automation(name)
        return context.json_result(ok=result.get("ok", False), message=result.get("message", "Automation finished."), result=result)

    @registry.register(
        name="list_automations",
        description="List saved automations.",
        parameters={"type": "object", "properties": {}, "additionalProperties": False},
    )
    def list_automations(context) -> dict:
        automations = context.scheduler.list_automations()
        return context.json_result(ok=True, message=f"Loaded {len(automations)} automations.", automations=automations)

    @registry.register(
        name="schedule_automation",
        description="Schedule a saved automation using an interval-based scheduler.",
        parameters={
            "type": "object",
            "properties": {
                "name": {"type": "string", "description": "Saved automation name"},
                "interval": {"type": "integer", "description": "Run every N units", "minimum": 1},
                "unit": {"type": "string", "enum": ["seconds", "minutes", "hours", "days"]},
                "at_time": {"type": "string", "description": "Optional HH:MM for daily jobs"},
            },
            "required": ["name", "interval", "unit"],
            "additionalProperties": False,
        },
        requires_confirmation=True,
        allow_in_schedule=False,
    )
    def schedule_automation(context, name: str, interval: int, unit: str, at_time: str | None = None) -> dict:
        automation = context.scheduler.get_automation(name)
        if not automation:
            return context.json_result(ok=False, message=f"Automation '{name}' was not found.")

        steps = automation.get("steps", [])
        for step in steps:
            spec = context.registry.get(step["tool_name"])
            if not spec.allow_in_schedule or spec.requires_confirmation:
                return context.json_result(
                    ok=False,
                    message=(
                        f"Automation '{name}' cannot be scheduled because it contains "
                        f"'{step['tool_name']}', which needs live approval."
                    ),
                )

        schedule_info = context.scheduler.create_schedule(
            automation_name=name,
            interval=interval,
            unit=unit,
            at_time=at_time,
        )
        return context.json_result(ok=True, message=f"Scheduled automation '{name}'.", schedule=schedule_info)

    @registry.register(
        name="list_schedules",
        description="List active schedules for saved automations.",
        parameters={"type": "object", "properties": {}, "additionalProperties": False},
    )
    def list_schedules(context) -> dict:
        schedules = context.scheduler.list_schedules()
        return context.json_result(ok=True, message=f"There are {len(schedules)} active schedules.", schedules=schedules)

    @registry.register(
        name="cancel_schedule",
        description="Cancel a scheduled automation by job id.",
        parameters={
            "type": "object",
            "properties": {"job_id": {"type": "string", "description": "Schedule job id"}},
            "required": ["job_id"],
            "additionalProperties": False,
        },
        requires_confirmation=True,
        allow_in_schedule=False,
    )
    def cancel_schedule(context, job_id: str) -> dict:
        cancelled = context.scheduler.cancel_schedule(job_id)
        if not cancelled:
            return context.json_result(ok=False, message=f"Schedule '{job_id}' was not found.")
        return context.json_result(ok=True, message=f"Cancelled schedule '{job_id}'.")


def _validate_steps(context, steps: list[dict]) -> None:
    for index, step in enumerate(steps, start=1):
        tool_name = step.get("tool_name")
        if not tool_name or not context.registry.has(tool_name):
            raise ValueError(f"Step {index} references unknown tool '{tool_name}'.")
        spec = context.registry.get(tool_name)
        if not spec.allow_in_automation:
            raise ValueError(f"Tool '{tool_name}' cannot be used in automations.")

