"""
FRIDAY Application Control Module
Handles opening and closing applications safely.
"""

import subprocess
import platform
import os
import psutil
from typing import Optional
from friday.config import APP_MAPPINGS


def open_application(app_name: str) -> str:
    """
    Open an application by name.
    For Chrome, uses Selenium with default profile to avoid profile selection.
    
    Args:
        app_name: Name of the application to open
        
    Returns:
        Success or error message
    """
    try:
        app_name_lower = app_name.lower()
        
        # Special handling for Chrome - use Selenium
        if 'chrome' in app_name_lower or 'google' in app_name_lower:
            from friday.actions.web_automation import start_browser
            return start_browser(headless=False)
        
        system = platform.system()
        
        # Normalize app name using mappings
        normalized_name = _normalize_app_name(app_name_lower)
        
        if system == "Windows":
            return _open_app_windows(normalized_name)
        elif system == "Darwin":  # macOS
            return _open_app_macos(normalized_name)
        elif system == "Linux":
            return _open_app_linux(normalized_name)
        else:
            return f"❌ Unsupported operating system: {system}"
            
    except Exception as e:
        return f"❌ Failed to open {app_name}: {str(e)}"


def close_application(app_name: str) -> str:
    """
    Close a running application by name.
    
    Args:
        app_name: Name of the application to close
        
    Returns:
        Success or error message
    """
    try:
        app_name_lower = app_name.lower()
        normalized_name = _normalize_app_name(app_name_lower)
        
        # Find and terminate the process
        closed_count = 0
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                process_name = proc.info['name'].lower()
                
                # Check if process name matches
                if any(app in process_name for app in normalized_name.split()):
                    proc.terminate()
                    closed_count += 1
                    print(f"Terminated process: {proc.info['name']} (PID: {proc.info['pid']})")
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        
        if closed_count > 0:
            return f"✅ Closed {closed_count} instance(s) of {app_name}"
        else:
            return f"⚠️  No running instances of {app_name} found"
            
    except Exception as e:
        return f"❌ Failed to close {app_name}: {str(e)}"


def _normalize_app_name(app_name: str) -> str:
    """
    Normalize application name using predefined mappings.
    
    Args:
        app_name: User-provided app name
        
    Returns:
        Normalized app name
    """
    for key, aliases in APP_MAPPINGS.items():
        if app_name in aliases or app_name == key:
            return aliases[0]  # Return primary name
    return app_name


def _open_app_windows(app_name: str) -> str:
    """Open application on Windows with smart path detection"""
    
    # Common application paths for popular programs
    app_locations = {
        'chrome': [
            r'C:\Program Files\Google\Chrome\Application\chrome.exe',
            r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe',
            os.path.expanduser(r'~\AppData\Local\Google\Chrome\Application\chrome.exe'),
        ],
        'firefox': [
            r'C:\Program Files\Mozilla Firefox\firefox.exe',
            r'C:\Program Files (x86)\Mozilla Firefox\firefox.exe',
        ],
        'edge': [
            r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe',
            r'C:\Program Files\Microsoft\Edge\Application\msedge.exe',
        ],
        'notepad': ['notepad.exe'],
        'notepad++': [
            r'C:\Program Files\Notepad++\notepad++.exe',
            r'C:\Program Files (x86)\Notepad++\notepad++.exe',
        ],
        'code': [
            os.path.expanduser(r'~\AppData\Local\Programs\Microsoft VS Code\Code.exe'),
            r'C:\Program Files\Microsoft VS Code\Code.exe',
        ],
        'vscode': [
            os.path.expanduser(r'~\AppData\Local\Programs\Microsoft VS Code\Code.exe'),
            r'C:\Program Files\Microsoft VS Code\Code.exe',
        ],
        'whatsapp': [
            os.path.expanduser(r'~\AppData\Local\WhatsApp\WhatsApp.exe'),
            os.path.expanduser(r'~\AppData\Local\Programs\WhatsApp\WhatsApp.exe'),
        ],
        'discord': [
            os.path.expanduser(r'~\AppData\Local\Discord\app-*\Discord.exe'),
            os.path.expanduser(r'~\AppData\Roaming\Discord\Discord.exe'),
        ],
        'spotify': [
            os.path.expanduser(r'~\AppData\Roaming\Spotify\Spotify.exe'),
        ],
        'telegram': [
            os.path.expanduser(r'~\AppData\Roaming\Telegram Desktop\Telegram.exe'),
        ],
    }
    
    app_name_lower = app_name.lower()
    
    # Check known locations first
    if app_name_lower in app_locations:
        for location in app_locations[app_name_lower]:
            # Use glob for wildcards
            if '*' in location:
                import glob
                matches = glob.glob(location)
                if matches:
                    location = matches[0]
            
            if os.path.exists(location):
                subprocess.Popen([location])
                return f"✅ Opening {app_name}..."

    # Check for UWP/Shell commands (e.g. ms-settings:)
    if "ms-" in app_name_lower or "shell:" in app_name_lower or app_name_lower == "whatsapp":
         try:
             # Try opening as a protocol or direct command
             if app_name_lower == "whatsapp":
                 os.system("start whatsapp:")
             else:
                 os.system(f"start {app_name}")
             return f"✅ Opening {app_name}..."
         except Exception:
             pass

    # Try generic 'start' command found in PATH
    try:
        # Use shell=True for internal commands and PATH resolution
        os.system(f"start {app_name}") 
        return f"✅ Opening {app_name}..."
    except Exception:
        pass
        
    return f"❌ {app_name} is not installed or not found in PATH."


def _open_app_macos(app_name: str) -> str:
    """Open application on macOS"""
    try:
        subprocess.Popen(["open", "-a", app_name])
        return f"✅ Opening {app_name}..."
    except Exception as e:
        return f"❌ Failed to open {app_name}: {str(e)}"


def _open_app_linux(app_name: str) -> str:
    """Open application on Linux"""
    try:
        subprocess.Popen([app_name], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return f"✅ Opening {app_name}..."
    except Exception as e:
        return f"❌ Failed to open {app_name}: {str(e)}"
