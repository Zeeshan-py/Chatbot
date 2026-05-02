from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable


ToolHandler = Callable[..., dict[str, Any]]


@dataclass(slots=True)
class ToolSpec:
    name: str
    description: str
    parameters: dict[str, Any]
    handler: ToolHandler
    requires_confirmation: bool = False
    allow_in_automation: bool = True
    allow_in_schedule: bool = True

    def to_openai_schema(self) -> dict[str, Any]:
        return {
            "type": "function",
            "name": self.name,
            "description": self.description,
            "parameters": self.parameters,
        }


class ToolRegistry:
    """Central registry for all tool definitions."""

    def __init__(self) -> None:
        self._tools: dict[str, ToolSpec] = {}

    def register(
        self,
        *,
        name: str,
        description: str,
        parameters: dict[str, Any],
        requires_confirmation: bool = False,
        allow_in_automation: bool = True,
        allow_in_schedule: bool = True,
    ) -> Callable[[ToolHandler], ToolHandler]:
        def decorator(func: ToolHandler) -> ToolHandler:
            self._tools[name] = ToolSpec(
                name=name,
                description=description,
                parameters=parameters,
                handler=func,
                requires_confirmation=requires_confirmation,
                allow_in_automation=allow_in_automation,
                allow_in_schedule=allow_in_schedule,
            )
            return func

        return decorator

    def get(self, name: str) -> ToolSpec:
        return self._tools[name]

    def has(self, name: str) -> bool:
        return name in self._tools

    def all(self) -> list[ToolSpec]:
        return list(self._tools.values())

    def schemas(self) -> list[dict[str, Any]]:
        return [tool.to_openai_schema() for tool in self._tools.values()]

