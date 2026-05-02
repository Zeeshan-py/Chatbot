from __future__ import annotations

import shutil
from pathlib import Path

from friday.permissions import PermissionError
from friday.tool_registry import ToolRegistry


def register(registry: ToolRegistry) -> None:
    @registry.register(
        name="list_directory",
        description="List files and folders in a directory.",
        parameters={
            "type": "object",
            "properties": {
                "directory_path": {"type": "string", "description": "Directory to inspect", "default": "."}
            },
            "additionalProperties": False,
        },
    )
    def list_directory(context, directory_path: str = ".") -> dict:
        directory = context.permissions.ensure_path_allowed(directory_path, action="list_directory")
        if not directory.exists():
            return context.json_result(ok=False, message=f"Directory not found: {directory}")
        if not directory.is_dir():
            return context.json_result(ok=False, message=f"Not a directory: {directory}")

        entries = []
        for item in sorted(directory.iterdir(), key=lambda entry: (not entry.is_dir(), entry.name.lower()))[:200]:
            entries.append(
                {
                    "name": item.name,
                    "type": "directory" if item.is_dir() else "file",
                    "size": item.stat().st_size if item.is_file() else None,
                }
            )
        return context.json_result(ok=True, message=f"Listed {len(entries)} items in {directory}.", items=entries)

    @registry.register(
        name="create_directory",
        description="Create a directory inside the allowed workspace.",
        parameters={
            "type": "object",
            "properties": {"directory_path": {"type": "string", "description": "Directory path to create"}},
            "required": ["directory_path"],
            "additionalProperties": False,
        },
    )
    def create_directory(context, directory_path: str) -> dict:
        directory = context.permissions.ensure_path_allowed(directory_path, action="create_directory")
        directory.mkdir(parents=True, exist_ok=True)
        return context.json_result(ok=True, message=f"Created directory {directory}.", path=str(directory))

    @registry.register(
        name="write_file",
        description="Create or overwrite a text file in an allowed directory.",
        parameters={
            "type": "object",
            "properties": {
                "file_path": {"type": "string", "description": "Target file path"},
                "content": {"type": "string", "description": "Text content to write"},
                "append": {"type": "boolean", "description": "Append instead of overwrite", "default": False},
            },
            "required": ["file_path", "content"],
            "additionalProperties": False,
        },
        requires_confirmation=True,
        allow_in_schedule=False,
    )
    def write_file(context, file_path: str, content: str, append: bool = False) -> dict:
        path = context.permissions.ensure_path_allowed(file_path, action="write_file")
        context.ensure_parent_directory(path)
        mode = "a" if append else "w"
        with path.open(mode, encoding="utf-8") as handle:
            handle.write(content)
        return context.json_result(ok=True, message=f"Wrote file {path}.", path=str(path))

    @registry.register(
        name="read_file",
        description="Read the contents of a text file from an allowed directory.",
        parameters={
            "type": "object",
            "properties": {"file_path": {"type": "string", "description": "File to read"}},
            "required": ["file_path"],
            "additionalProperties": False,
        },
    )
    def read_file(context, file_path: str) -> dict:
        path = context.permissions.ensure_path_allowed(file_path, action="read_file")
        if not path.exists() or not path.is_file():
            return context.json_result(ok=False, message=f"File not found: {path}")
        content = path.read_text(encoding="utf-8", errors="ignore")
        trimmed = content[: context.config.security.max_file_chars]
        return context.json_result(ok=True, message=f"Read {path}.", path=str(path), content=trimmed)

    @registry.register(
        name="move_path",
        description="Move or rename a file or directory inside allowed roots.",
        parameters={
            "type": "object",
            "properties": {
                "source_path": {"type": "string", "description": "Existing file or directory"},
                "destination_path": {"type": "string", "description": "New path"},
            },
            "required": ["source_path", "destination_path"],
            "additionalProperties": False,
        },
        requires_confirmation=True,
        allow_in_schedule=False,
    )
    def move_path(context, source_path: str, destination_path: str) -> dict:
        source = context.permissions.ensure_path_allowed(source_path, action="move_path")
        destination = context.permissions.ensure_path_allowed(destination_path, action="move_path")
        if not source.exists():
            return context.json_result(ok=False, message=f"Source path not found: {source}")
        context.ensure_parent_directory(destination)
        shutil.move(str(source), str(destination))
        return context.json_result(ok=True, message=f"Moved {source} to {destination}.")

    @registry.register(
        name="delete_path",
        description="Delete a file or directory in an allowed root.",
        parameters={
            "type": "object",
            "properties": {"path": {"type": "string", "description": "File or directory to delete"}},
            "required": ["path"],
            "additionalProperties": False,
        },
        requires_confirmation=True,
        allow_in_schedule=False,
    )
    def delete_path(context, path: str) -> dict:
        target = context.permissions.ensure_path_allowed(path, action="delete_path")
        if not target.exists():
            return context.json_result(ok=False, message=f"Path not found: {target}")
        if target.is_dir():
            shutil.rmtree(target)
        else:
            target.unlink()
        return context.json_result(ok=True, message=f"Deleted {target}.")

    @registry.register(
        name="search_files",
        description="Search for files by partial name within an allowed directory tree.",
        parameters={
            "type": "object",
            "properties": {
                "directory_path": {"type": "string", "description": "Root directory to search", "default": "."},
                "name_contains": {"type": "string", "description": "Case-insensitive substring to match"},
                "file_extension": {"type": "string", "description": "Optional extension filter such as .py"},
                "max_results": {"type": "integer", "description": "Maximum results", "default": 25, "minimum": 1, "maximum": 200},
            },
            "required": ["name_contains"],
            "additionalProperties": False,
        },
    )
    def search_files(
        context,
        name_contains: str,
        directory_path: str = ".",
        file_extension: str | None = None,
        max_results: int = 25,
    ) -> dict:
        directory = context.permissions.ensure_path_allowed(directory_path, action="search_files")
        matches = []
        extension = file_extension.lower() if file_extension else None
        needle = name_contains.lower()
        for item in directory.rglob("*"):
            if len(matches) >= max_results:
                break
            if not item.is_file():
                continue
            if needle not in item.name.lower():
                continue
            if extension and item.suffix.lower() != extension:
                continue
            matches.append(str(item))
        return context.json_result(
            ok=True,
            message=f"Found {len(matches)} file(s) matching '{name_contains}'.",
            matches=matches,
        )

    @registry.register(
        name="summarize_file",
        description="Read a file and return a concise summary of its contents.",
        parameters={
            "type": "object",
            "properties": {
                "file_path": {"type": "string", "description": "File to summarize"},
                "purpose": {"type": "string", "description": "What the summary should focus on", "default": "general review"},
            },
            "required": ["file_path"],
            "additionalProperties": False,
        },
    )
    def summarize_file(context, file_path: str, purpose: str = "general review") -> dict:
        path = context.permissions.ensure_path_allowed(file_path, action="summarize_file")
        if not path.exists() or not path.is_file():
            return context.json_result(ok=False, message=f"File not found: {path}")
        content = path.read_text(encoding="utf-8", errors="ignore")
        summary = context.summarize_text(content, purpose=purpose)
        return context.json_result(ok=True, message=f"Summarized {path}.", summary=summary, path=str(path))

