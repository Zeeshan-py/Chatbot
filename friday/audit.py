from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


class AuditLogger:
    """Append-only JSONL audit log for all tool activity."""

    def __init__(self, log_path: Path) -> None:
        self.log_path = log_path
        self.log_path.parent.mkdir(parents=True, exist_ok=True)

    def log(self, *, event: str, payload: dict[str, Any]) -> None:
        record = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "event": event,
            "payload": payload,
        }
        with self.log_path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(record, ensure_ascii=True) + "\n")

