from __future__ import annotations

from friday.tool_registry import ToolRegistry
from friday.tools import application_tools, automation_tools, file_tools, system_tools


def build_registry() -> ToolRegistry:
    registry = ToolRegistry()
    application_tools.register(registry)
    system_tools.register(registry)
    file_tools.register(registry)
    automation_tools.register(registry)
    return registry

