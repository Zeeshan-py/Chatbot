from __future__ import annotations

from collections import deque
from typing import Deque


class ConversationMemory:
    """Bounded in-memory conversation history."""

    def __init__(self, max_messages: int = 24) -> None:
        self.max_messages = max_messages
        self._messages: Deque[dict[str, str]] = deque(maxlen=max_messages)

    def add(self, role: str, content: str) -> None:
        self._messages.append({"role": role, "content": content})

    def clear(self) -> None:
        self._messages.clear()

    def to_openai_input(self) -> list[dict[str, str]]:
        return list(self._messages)

    @property
    def messages(self) -> list[dict[str, str]]:
        return list(self._messages)

