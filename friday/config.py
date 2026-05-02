from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


def _existing_path(raw_path: str) -> Path:
    return Path(os.path.expandvars(raw_path)).expanduser().resolve()


def _split_paths(raw_value: str | None) -> list[Path]:
    if not raw_value:
        return []
    return [_existing_path(part.strip()) for part in raw_value.split(os.pathsep) if part.strip()]


@dataclass(frozen=True)
class SecurityConfig:
    allowed_roots: tuple[Path, ...]
    blocked_roots: tuple[Path, ...]
    confirmation_actions: frozenset[str]
    blocked_command_patterns: tuple[str, ...]
    max_file_chars: int = 120_000
    max_summary_chars: int = 30_000


@dataclass(frozen=True)
class AppConfig:
    project_root: Path
    data_dir: Path
    log_dir: Path
    action_log_path: Path
    openai_api_key: str | None
    openai_model: str
    memory_window: int
    max_tool_rounds: int
    scheduler_poll_interval: float
    voice_output_enabled: bool
    security: SecurityConfig
    app_aliases: dict[str, tuple[str, ...]]
    app_launchers: dict[str, tuple[str, ...]]
    system_prompt: str


def load_config() -> AppConfig:
    project_root = Path(__file__).resolve().parent.parent
    load_dotenv(project_root / ".env")

    data_dir = project_root / "assistant_data"
    log_dir = project_root / "logs"
    data_dir.mkdir(exist_ok=True)
    log_dir.mkdir(exist_ok=True)

    home = Path.home().resolve()
    extra_allowed = _split_paths(os.getenv("FRIDAY_ALLOWED_ROOTS"))
    allowed_roots = tuple(
        dict.fromkeys(
            [
                project_root.resolve(),
                (home / "Desktop").resolve(),
                (home / "Documents").resolve(),
                (home / "Downloads").resolve(),
                *extra_allowed,
            ]
        )
    )

    blocked_roots = tuple(
        dict.fromkeys(
            [
                Path(os.environ.get("WINDIR", r"C:\Windows")).resolve(),
                Path(r"C:\Program Files").resolve(),
                Path(r"C:\Program Files (x86)").resolve(),
                (home / ".ssh").resolve(),
                (home / ".aws").resolve(),
                (home / ".gnupg").resolve(),
                (home / "AppData" / "Roaming" / "Microsoft" / "Credentials").resolve(),
            ]
        )
    )

    security = SecurityConfig(
        allowed_roots=allowed_roots,
        blocked_roots=blocked_roots,
        confirmation_actions=frozenset(
            {
                "close_application",
                "execute_system_command",
                "write_file",
                "move_path",
                "delete_path",
                "save_automation",
                "run_automation",
                "schedule_automation",
                "cancel_schedule",
            }
        ),
        blocked_command_patterns=(
            r"\brm\s+-rf\b",
            r"\bdel\s+/[a-z]*s[a-z]*\b",
            r"\bformat\b",
            r"\bshutdown\b",
            r"\brestart-computer\b",
            r"\breg\s+delete\b",
            r"\bsc\s+delete\b",
            r"\bcipher\s+/w\b",
            r"\btakeown\b",
            r"\bicacls\b.+\b/grant\b",
        ),
    )

    app_aliases = {
        "chrome": ("chrome", "google chrome"),
        "code": ("code", "vscode", "visual studio code", "vs code"),
        "vscode": ("code", "vscode", "visual studio code", "vs code"),
        "notepad": ("notepad",),
        "explorer": ("explorer", "file explorer"),
    }

    app_launchers = {
        "chrome": (
            r"%ProgramFiles%\Google\Chrome\Application\chrome.exe",
            r"%ProgramFiles(x86)%\Google\Chrome\Application\chrome.exe",
        ),
        "google chrome": (
            r"%ProgramFiles%\Google\Chrome\Application\chrome.exe",
            r"%ProgramFiles(x86)%\Google\Chrome\Application\chrome.exe",
        ),
        "code": (
            r"%LocalAppData%\Programs\Microsoft VS Code\Code.exe",
            r"%ProgramFiles%\Microsoft VS Code\Code.exe",
        ),
        "vscode": (
            r"%LocalAppData%\Programs\Microsoft VS Code\Code.exe",
            r"%ProgramFiles%\Microsoft VS Code\Code.exe",
        ),
        "visual studio code": (
            r"%LocalAppData%\Programs\Microsoft VS Code\Code.exe",
            r"%ProgramFiles%\Microsoft VS Code\Code.exe",
        ),
        "vs code": (
            r"%LocalAppData%\Programs\Microsoft VS Code\Code.exe",
            r"%ProgramFiles%\Microsoft VS Code\Code.exe",
        ),
        "notepad": ("notepad.exe",),
        "explorer": ("explorer.exe",),
        "file explorer": ("explorer.exe",),
    }

    system_prompt = """You are FRIDAY, a careful Windows desktop AI assistant.

You can use tools to act on the user's machine, but safety rules are strict:
- Never claim a tool succeeded until you have seen its output.
- Prefer the smallest safe action that solves the user's request.
- Ask for tool use only when needed.
- Treat file writes, deletes, moves, automation creation, scheduling, and system commands as sensitive.
- Respect protected directories and never try to bypass the permission layer.
- When summarizing files, be concise and practical.
- When a tool is denied, explain the denial and offer a safer alternative.
"""

    return AppConfig(
        project_root=project_root,
        data_dir=data_dir,
        log_dir=log_dir,
        action_log_path=log_dir / "assistant_actions.jsonl",
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        openai_model=os.getenv("OPENAI_MODEL", "gpt-5.4-mini"),
        memory_window=int(os.getenv("FRIDAY_MEMORY_WINDOW", "24")),
        max_tool_rounds=int(os.getenv("FRIDAY_MAX_TOOL_ROUNDS", "8")),
        scheduler_poll_interval=float(os.getenv("FRIDAY_SCHEDULER_POLL_SECONDS", "1.0")),
        voice_output_enabled=os.getenv("FRIDAY_VOICE_OUTPUT", "false").lower() == "true",
        security=security,
        app_aliases=app_aliases,
        app_launchers=app_launchers,
        system_prompt=system_prompt,
    )


config = load_config()
