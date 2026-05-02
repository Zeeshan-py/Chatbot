from __future__ import annotations

import os
import sys
from typing import Optional

from colorama import Fore, Style, init


init(autoreset=True)


def print_header() -> None:
    print(
        f"{Fore.CYAN}============================================================\n"
        f"FRIDAY\n"
        f"Secure AI Desktop Assistant\n"
        f"============================================================{Style.RESET_ALL}"
    )


def print_info(message: str) -> None:
    print(f"{Fore.BLUE}[info]{Style.RESET_ALL} {message}")


def print_success(message: str) -> None:
    print(f"{Fore.GREEN}[ok]{Style.RESET_ALL} {message}")


def print_error(message: str) -> None:
    print(f"{Fore.RED}[error]{Style.RESET_ALL} {message}")


def print_warning(message: str) -> None:
    print(f"{Fore.YELLOW}[warn]{Style.RESET_ALL} {message}")


def print_ai_response(message: str) -> None:
    print(f"{Fore.MAGENTA}FRIDAY:{Style.RESET_ALL} {message}")


def print_divider() -> None:
    print(f"{Fore.CYAN}{'-' * 60}{Style.RESET_ALL}")


def get_user_input(prompt: str = "You") -> Optional[str]:
    try:
        return input(f"{Fore.CYAN}{prompt}:{Style.RESET_ALL} ").strip()
    except (KeyboardInterrupt, EOFError):
        print()
        return None


def show_help() -> None:
    print(
        """
Core usage:
  - Ask naturally: open chrome, write notes.txt, summarize README.md
  - FRIDAY uses OpenAI tool calling to plan and execute registered tools

Capabilities:
  - Open and close supported desktop apps
  - Run confirmed system commands through subprocess
  - Create, read, move, delete, and search files in allowed roots
  - Summarize file contents
  - Save, run, and schedule automations
  - Optional speech recognition and text-to-speech

Special commands:
  - help
  - reset
  - tools
  - automations
  - schedules
  - voice on / voice off
  - listen
  - clear
  - exit

Security:
  - Sensitive actions require confirmation
  - Protected directories are blocked unless explicitly allowed in config
  - All tool actions are logged to logs/assistant_actions.jsonl
""".strip()
    )


def clear_screen() -> None:
    os.system("cls" if sys.platform == "win32" else "clear")
