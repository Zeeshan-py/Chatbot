from __future__ import annotations

import json
import threading
import time
import uuid
from pathlib import Path
from typing import Any, Callable

import schedule


class SchedulerManager:
    """Persistent automation registry plus in-process scheduler."""

    def __init__(self, data_dir: Path, poll_interval: float = 1.0) -> None:
        self.data_dir = data_dir
        self.poll_interval = poll_interval
        self.automations_path = data_dir / "automations.json"
        self.schedules_path = data_dir / "schedules.json"
        self.data_dir.mkdir(parents=True, exist_ok=True)

        self._runner: Callable[[str], dict[str, Any]] | None = None
        self._stop_event = threading.Event()
        self._thread: threading.Thread | None = None
        self._jobs: dict[str, schedule.Job] = {}
        self._automations = self._load_json(self.automations_path, {})
        self._schedule_specs = self._load_json(self.schedules_path, [])
        self._rehydrate_jobs()

    def set_runner(self, runner: Callable[[str], dict[str, Any]]) -> None:
        self._runner = runner

    def start(self) -> None:
        if self._thread and self._thread.is_alive():
            return
        self._thread = threading.Thread(target=self._loop, daemon=True)
        self._thread.start()

    def stop(self) -> None:
        self._stop_event.set()
        if self._thread and self._thread.is_alive():
            self._thread.join(timeout=2)

    def save_automation(self, name: str, description: str, steps: list[dict[str, Any]]) -> dict[str, Any]:
        self._automations[name] = {"description": description, "steps": steps}
        self._write_json(self.automations_path, self._automations)
        return {"name": name, "description": description, "step_count": len(steps)}

    def get_automation(self, name: str) -> dict[str, Any] | None:
        return self._automations.get(name)

    def list_automations(self) -> list[dict[str, Any]]:
        return [
            {
                "name": name,
                "description": details.get("description", ""),
                "step_count": len(details.get("steps", [])),
            }
            for name, details in sorted(self._automations.items())
        ]

    def run_automation(self, name: str) -> dict[str, Any]:
        if not self._runner:
            return {"ok": False, "message": "Automation runner is not configured."}
        return self._runner(name)

    def create_schedule(
        self,
        *,
        automation_name: str,
        interval: int,
        unit: str,
        at_time: str | None = None,
    ) -> dict[str, Any]:
        job_id = str(uuid.uuid4())[:8]
        spec = {
            "job_id": job_id,
            "automation_name": automation_name,
            "interval": interval,
            "unit": unit,
            "at_time": at_time,
        }
        job = self._build_job(spec)
        self._jobs[job_id] = job
        self._schedule_specs.append(spec)
        self._write_json(self.schedules_path, self._schedule_specs)
        return spec

    def list_schedules(self) -> list[dict[str, Any]]:
        return list(self._schedule_specs)

    def cancel_schedule(self, job_id: str) -> bool:
        job = self._jobs.pop(job_id, None)
        if job:
            schedule.cancel_job(job)
        before = len(self._schedule_specs)
        self._schedule_specs = [spec for spec in self._schedule_specs if spec["job_id"] != job_id]
        if len(self._schedule_specs) != before:
            self._write_json(self.schedules_path, self._schedule_specs)
            return True
        return False

    def _rehydrate_jobs(self) -> None:
        for spec in self._schedule_specs:
            self._jobs[spec["job_id"]] = self._build_job(spec)

    def _build_job(self, spec: dict[str, Any]) -> schedule.Job:
        interval = max(1, int(spec["interval"]))
        unit = spec["unit"]
        if unit not in {"seconds", "minutes", "hours", "days"}:
            raise ValueError(f"Unsupported schedule unit: {unit}")

        every = getattr(schedule.every(interval), unit)
        if unit == "days" and spec.get("at_time"):
            every = every.at(spec["at_time"])
        return every.do(self._run_scheduled_automation, spec["automation_name"])

    def _run_scheduled_automation(self, automation_name: str) -> None:
        if self._runner:
            self._runner(automation_name)

    def _loop(self) -> None:
        while not self._stop_event.is_set():
            schedule.run_pending()
            time.sleep(self.poll_interval)

    @staticmethod
    def _load_json(path: Path, fallback: Any) -> Any:
        if not path.exists():
            return fallback
        with path.open("r", encoding="utf-8") as handle:
            return json.load(handle)

    @staticmethod
    def _write_json(path: Path, data: Any) -> None:
        with path.open("w", encoding="utf-8") as handle:
            json.dump(data, handle, indent=2)

