from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Callable

from friday.config import AppConfig


class PermissionError(RuntimeError):
    pass


class PermissionManager:
    """Validates access to risky operations before tools execute."""

    def __init__(
        self,
        config: AppConfig,
        confirm_callback: Callable[[str], bool] | None = None,
    ) -> None:
        self.config = config
        self.confirm_callback = confirm_callback or self._default_confirm

    def resolve_path(self, raw_path: str) -> Path:
        path = Path(raw_path).expanduser()
        if not path.is_absolute():
            path = (self.config.project_root / path).resolve()
        else:
            path = path.resolve()
        return path

    def ensure_path_allowed(self, raw_path: str, *, action: str) -> Path:
        path = self.resolve_path(raw_path)

        for blocked in self.config.security.blocked_roots:
            if self._is_relative_to(path, blocked):
                raise PermissionError(
                    f"{action} blocked: '{path}' is inside a protected directory."
                )

        if not any(self._is_relative_to(path, root) for root in self.config.security.allowed_roots):
            roots = ", ".join(str(root) for root in self.config.security.allowed_roots)
            raise PermissionError(
                f"{action} blocked: '{path}' is outside allowed roots. Allowed roots: {roots}"
            )

        return path

    def ensure_command_allowed(self, command: str) -> None:
        lowered = command.lower()
        for pattern in self.config.security.blocked_command_patterns:
            if re.search(pattern, lowered):
                raise PermissionError(
                    f"Command blocked by safety policy because it matched '{pattern}'."
                )

    def confirm(self, action: str, summary: str) -> None:
        if action not in self.config.security.confirmation_actions:
            return
        approved = self.confirm_callback(
            f"Confirmation required for '{action}'. {summary}. Proceed? [y/N]: "
        )
        if not approved:
            raise PermissionError(f"{action} cancelled by user.")

    @staticmethod
    def _is_relative_to(path: Path, base: Path) -> bool:
        try:
            path.relative_to(base)
            return True
        except ValueError:
            return False

    @staticmethod
    def _default_confirm(prompt: str) -> bool:
        if not sys.stdin or not sys.stdin.isatty():
            return False
        answer = input(prompt).strip().lower()
        return answer in {"y", "yes"}

