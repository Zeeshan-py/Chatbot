from __future__ import annotations

import platform
import subprocess
from datetime import datetime

from friday.permissions import PermissionError
from friday.tool_registry import ToolRegistry


def register(registry: ToolRegistry) -> None:
    @registry.register(
        name="execute_system_command",
        description="Run a system command through subprocess. This tool is dangerous and always asks for confirmation.",
        parameters={
            "type": "object",
            "properties": {
                "command": {"type": "string", "description": "PowerShell command on Windows or shell command on Unix"},
                "timeout_seconds": {
                    "type": "integer",
                    "description": "Timeout in seconds, default 20",
                    "minimum": 1,
                    "maximum": 120,
                },
            },
            "required": ["command"],
            "additionalProperties": False,
        },
        requires_confirmation=True,
        allow_in_schedule=False,
    )
    def execute_system_command(context, command: str, timeout_seconds: int = 20) -> dict:
        context.permissions.ensure_command_allowed(command)
        context.audit.log(event="tool_requested", payload={"tool": "execute_system_command", "command": command})

        if platform.system() == "Windows":
            shell_command = ["powershell", "-NoProfile", "-Command", command]
        else:
            shell_command = ["/bin/sh", "-lc", command]

        result = subprocess.run(
            shell_command,
            capture_output=True,
            text=True,
            timeout=timeout_seconds,
        )
        output = (result.stdout or result.stderr).strip()
        message = "Command completed successfully." if result.returncode == 0 else "Command finished with a non-zero exit code."
        return context.json_result(
            ok=result.returncode == 0,
            message=message,
            return_code=result.returncode,
            output=output[:6000],
        )

    @registry.register(
        name="get_current_time",
        description="Get the current local date and time.",
        parameters={"type": "object", "properties": {}, "additionalProperties": False},
    )
    def get_current_time(context) -> dict:
        now = datetime.now().strftime("%A, %B %d, %Y %I:%M:%S %p")
        return context.json_result(ok=True, message=now, current_time=now)

