from __future__ import annotations

import os
import subprocess
from pathlib import Path

import psutil

from friday.tool_registry import ToolRegistry


def register(registry: ToolRegistry) -> None:
    @registry.register(
        name="open_application",
        description="Open a desktop application such as Chrome, VS Code, Notepad, or Explorer.",
        parameters={
            "type": "object",
            "properties": {
                "app_name": {"type": "string", "description": "Friendly app name such as chrome or vscode"},
                "arguments": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Optional command line arguments",
                },
            },
            "required": ["app_name"],
            "additionalProperties": False,
        },
    )
    def open_application(context, app_name: str, arguments: list[str] | None = None) -> dict:
        target = _resolve_application(context.config, app_name)
        context.audit.log(event="tool_requested", payload={"tool": "open_application", "app_name": app_name})
        subprocess.Popen([str(target), *(arguments or [])], shell=False)
        return context.json_result(ok=True, message=f"Opened {app_name}.", path=str(target))

    @registry.register(
        name="close_application",
        description="Close a running desktop application by friendly name or process name.",
        parameters={
            "type": "object",
            "properties": {
                "app_name": {"type": "string", "description": "Friendly app name such as chrome or code"}
            },
            "required": ["app_name"],
            "additionalProperties": False,
        },
        requires_confirmation=True,
        allow_in_schedule=False,
    )
    def close_application(context, app_name: str) -> dict:
        aliases = context.config.app_aliases.get(app_name.lower(), (app_name.lower(),))
        closed = 0
        for proc in psutil.process_iter(["name"]):
            try:
                name = (proc.info.get("name") or "").lower()
                if any(alias in name for alias in aliases):
                    proc.terminate()
                    closed += 1
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

        if not closed:
            return context.json_result(ok=False, message=f"No running process matched '{app_name}'.")
        return context.json_result(ok=True, message=f"Closed {closed} process(es) for {app_name}.")


def _resolve_application(config, app_name: str) -> Path:
    normalized = app_name.lower().strip()
    candidates = config.app_launchers.get(normalized)
    if not candidates:
        aliases = config.app_aliases.get(normalized, ())
        for alias in aliases:
            candidates = config.app_launchers.get(alias)
            if candidates:
                break

    if not candidates:
        raise FileNotFoundError(f"Unsupported application '{app_name}'. Add it to app_launchers in config.py.")

    for candidate in candidates:
        expanded = Path(os.path.expandvars(candidate)).expanduser()
        if expanded.exists():
            return expanded

    if len(candidates) == 1 and candidates[0].lower().endswith(".exe"):
        return Path(candidates[0])

    raise FileNotFoundError(f"Configured launcher for '{app_name}' was not found on disk.")

