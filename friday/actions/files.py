"""
FRIDAY File Management Module
Handles file and folder operations with safety checks.
"""

import os
import shutil
from pathlib import Path
from typing import List, Optional
from friday.config import SAFETY_SETTINGS


def create_file(file_path: str, content: str = "") -> str:
    """
    Create a new file with optional content.
    
    Args:
        file_path: Path where file should be created
        content: Optional content to write to file
        
    Returns:
        Success or error message
    """
    try:
        path = Path(file_path)
        
        # Security check
        if not _is_path_safe(path):
            return f"❌ Security Error: Cannot create file in protected location"
        
        # Create parent directories if they don't exist
        path.parent.mkdir(parents=True, exist_ok=True)
        
        # Create file
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return f"✅ Created file: {path.absolute()}"
        
    except Exception as e:
        return f"❌ Failed to create file: {str(e)}"


def create_folder(folder_path: str) -> str:
    """
    Create a new folder.
    
    Args:
        folder_path: Path where folder should be created
        
    Returns:
        Success or error message
    """
    try:
        path = Path(folder_path)
        
        # Security check
        if not _is_path_safe(path):
            return f"❌ Security Error: Cannot create folder in protected location"
        
        # Create folder
        path.mkdir(parents=True, exist_ok=True)
        
        return f"✅ Created folder: {path.absolute()}"
        
    except Exception as e:
        return f"❌ Failed to create folder: {str(e)}"


def delete_file(file_path: str) -> str:
    """
    Delete a file.
    
    Args:
        file_path: Path of file to delete
        
    Returns:
        Success or error message
    """
    try:
        path = Path(file_path)
        
        # Security checks
        if not _is_path_safe(path):
            return f"❌ Security Error: Cannot delete file in protected location"
        
        if not path.exists():
            return f"⚠️  File does not exist: {path}"
        
        if not path.is_file():
            return f"❌ Path is not a file: {path}"
        
        # Delete file
        path.unlink()
        
        return f"✅ Deleted file: {path.absolute()}"
        
    except Exception as e:
        return f"❌ Failed to delete file: {str(e)}"


def delete_folder(folder_path: str) -> str:
    """
    Delete a folder and its contents.
    
    Args:
        folder_path: Path of folder to delete
        
    Returns:
        Success or error message
    """
    try:
        path = Path(folder_path)
        
        # Security checks
        if not _is_path_safe(path):
            return f"❌ Security Error: Cannot delete folder in protected location"
        
        if not path.exists():
            return f"⚠️  Folder does not exist: {path}"
        
        if not path.is_dir():
            return f"❌ Path is not a folder: {path}"
        
        # Delete folder
        shutil.rmtree(path)
        
        return f"✅ Deleted folder: {path.absolute()}"
        
    except Exception as e:
        return f"❌ Failed to delete folder: {str(e)}"


def move_file(source: str, destination: str) -> str:
    """
    Move a file from source to destination.
    
    Args:
        source: Source file path
        destination: Destination file path
        
    Returns:
        Success or error message
    """
    try:
        src_path = Path(source)
        dst_path = Path(destination)
        
        # Security checks
        if not _is_path_safe(src_path) or not _is_path_safe(dst_path):
            return f"❌ Security Error: Cannot move file in/to protected location"
        
        if not src_path.exists():
            return f"⚠️  Source file does not exist: {src_path}"
        
        # Create destination directory if needed
        dst_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Move file
        shutil.move(str(src_path), str(dst_path))
        
        return f"✅ Moved {src_path.name} to {dst_path.absolute()}"
        
    except Exception as e:
        return f"❌ Failed to move file: {str(e)}"


def copy_file(source: str, destination: str) -> str:
    """
    Copy a file from source to destination.
    
    Args:
        source: Source file path
        destination: Destination file path
        
    Returns:
        Success or error message
    """
    try:
        src_path = Path(source)
        dst_path = Path(destination)
        
        # Security checks
        if not _is_path_safe(src_path) or not _is_path_safe(dst_path):
            return f"❌ Security Error: Cannot copy file in/to protected location"
        
        if not src_path.exists():
            return f"⚠️  Source file does not exist: {src_path}"
        
        # Create destination directory if needed
        dst_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Copy file
        shutil.copy2(str(src_path), str(dst_path))
        
        return f"✅ Copied {src_path.name} to {dst_path.absolute()}"
        
    except Exception as e:
        return f"❌ Failed to copy file: {str(e)}"


def list_files(directory_path: str = ".") -> str:
    """
    List files in a directory.
    
    Args:
        directory_path: Path of directory to list
        
    Returns:
        Formatted list of files and folders
    """
    try:
        path = Path(directory_path)
        
        if not path.exists():
            return f"⚠️  Directory does not exist: {path}"
        
        if not path.is_dir():
            return f"❌ Path is not a directory: {path}"
        
        # List contents
        items = list(path.iterdir())
        
        if not items:
            return f"📁 {path.absolute()} is empty"
        
        # Separate folders and files
        folders = [item for item in items if item.is_dir()]
        files = [item for item in items if item.is_file()]
        
        result = [f"📁 {path.absolute()}\n"]
        
        if folders:
            result.append("Folders:")
            for folder in sorted(folders):
                result.append(f"  📂 {folder.name}")
        
        if files:
            result.append("\nFiles:")
            for file in sorted(files):
                size = file.stat().st_size
                size_str = _format_file_size(size)
                result.append(f"  📄 {file.name} ({size_str})")
        
        result.append(f"\nTotal: {len(folders)} folder(s), {len(files)} file(s)")
        
        return "\n".join(result)
        
    except Exception as e:
        return f"❌ Failed to list directory: {str(e)}"


def organize_downloads(downloads_path: Optional[str] = None) -> str:
    """
    Organize downloads folder by file type.
    
    Args:
        downloads_path: Optional custom downloads path
        
    Returns:
        Success or error message
    """
    try:
        # Use default downloads folder if not specified
        if downloads_path is None:
            downloads_path = str(Path.home() / "Downloads")
        
        path = Path(downloads_path)
        
        if not path.exists() or not path.is_dir():
            return f"⚠️  Downloads folder not found: {path}"
        
        # File type categories
        categories = {
            "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".ico", ".webp"],
            "Documents": [".pdf", ".doc", ".docx", ".txt", ".rtf", ".odt"],
            "Spreadsheets": [".xls", ".xlsx", ".csv"],
            "Presentations": [".ppt", ".pptx"],
            "Videos": [".mp4", ".avi", ".mkv", ".mov", ".wmv", ".flv", ".webm"],
            "Audio": [".mp3", ".wav", ".flac", ".m4a", ".aac", ".ogg"],
            "Archives": [".zip", ".rar", ".7z", ".tar", ".gz"],
            "Programs": [".exe", ".msi", ".dmg", ".pkg", ".deb", ".rpm"],
            "Code": [".py", ".js", ".html", ".css", ".java", ".cpp", ".c", ".go", ".rs"],
        }
        
        moved_count = 0
        
        # Organize files
        for item in path.iterdir():
            if item.is_file():
                file_ext = item.suffix.lower()
                
                # Find category
                category = "Other"
                for cat_name, extensions in categories.items():
                    if file_ext in extensions:
                        category = cat_name
                        break
                
                # Create category folder
                category_folder = path / category
                category_folder.mkdir(exist_ok=True)
                
                # Move file
                try:
                    destination = category_folder / item.name
                    
                    # Handle duplicate names
                    counter = 1
                    while destination.exists():
                        stem = item.stem
                        destination = category_folder / f"{stem}_{counter}{item.suffix}"
                        counter += 1
                    
                    shutil.move(str(item), str(destination))
                    moved_count += 1
                except Exception as e:
                    print(f"Could not move {item.name}: {e}")
        
        return f"✅ Organized {moved_count} file(s) in Downloads folder"
        
    except Exception as e:
        return f"❌ Failed to organize downloads: {str(e)}"


def _is_path_safe(path: Path) -> bool:
    """
    Check if a path is safe to modify (not in protected system directories).
    
    Args:
        path: Path to check
        
    Returns:
        True if safe, False otherwise
    """
    try:
        absolute_path = str(path.absolute())
        
        # Check against blocked paths
        for blocked in SAFETY_SETTINGS["blocked_paths"]:
            if absolute_path.startswith(blocked):
                return False
        
        return True
    except Exception:
        return False


def _format_file_size(size_bytes: int) -> str:
    """Format file size in human-readable format"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} TB"
