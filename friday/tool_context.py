from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from openai import OpenAI

from friday.audit import AuditLogger
from friday.config import AppConfig
from friday.memory import ConversationMemory
from friday.permissions import PermissionManager


@dataclass
class ToolContext:
    config: AppConfig
    permissions: PermissionManager
    audit: AuditLogger
    memory: ConversationMemory
    scheduler: Any
    voice: Any
    registry: Any
    client: OpenAI | None = None

    def summarize_text(self, text: str, *, purpose: str) -> str:
        if not text.strip():
            return "The file is empty."

        if not self.client:
            lines = [line.strip() for line in text.splitlines() if line.strip()]
            preview = lines[:5]
            summary = [
                f"Local summary for {purpose}:",
                f"- Characters: {len(text)}",
                f"- Lines: {len(text.splitlines())}",
            ]
            if preview:
                summary.append("- Preview:")
                summary.extend(f"  - {line[:120]}" for line in preview)
            return "\n".join(summary)

        response = self.client.responses.create(
            model=self.config.openai_model,
            instructions=(
                "Summarize the supplied file content for a desktop assistant user. "
                "Mention key points, risks, and any action items in concise bullets."
            ),
            input=f"Purpose: {purpose}\n\nContent:\n{text[: self.config.security.max_summary_chars]}",
        )
        return response.output_text.strip()

    def json_result(self, *, ok: bool, message: str, **extra: Any) -> dict[str, Any]:
        payload = {"ok": ok, "message": message}
        payload.update(extra)
        return payload

    def serialize_tool_output(self, result: dict[str, Any]) -> str:
        return json.dumps(result, ensure_ascii=True)

    def ensure_parent_directory(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)

