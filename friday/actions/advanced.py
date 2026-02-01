"""
FRIDAY Advanced Control Module
⚠️ WARNING: Allows broader system control
Use with caution - can execute system commands
"""

import subprocess
import os
import platform
from typing import Dict, Any


def execute_system_command(command: str, shell: bool = True) -> str:
    """
    Execute arbitrary system command.
    ⚠️ WARNING: This is powerful and potentially dangerous!
    
    Args:
        command: System command to execute
        shell: Execute in shell (default True)
        
    Returns:
        Command output or error message
    """
    try:
        result = subprocess.run(
            command,
            shell=shell,
            capture_output=True,
            text=True,
            timeout=30
        )
        
        output = result.stdout if result.stdout else result.stderr
        
        if result.returncode == 0:
            return f"✅ Command executed successfully:\n{output}"
        else:
            return f"⚠️ Command completed with warnings:\n{output}"
            
    except subprocess.TimeoutExpired:
        return "❌ Command timed out (30s limit)"
    except Exception as e:
        return f"❌ Failed to execute command: {str(e)}"


def run_python_code(code: str) -> str:
    """
    Execute Python code dynamically.
    ⚠️ WARNING: Can execute any Python code!
    
    Args:
        code: Python code to execute
        
    Returns:
        Execution result or error
    """
    try:
        # Create a restricted namespace
        namespace = {
            '__builtins__': __builtins__,
            'os': os,
            'platform': platform,
            'subprocess': subprocess,
        }
        
        # Capture output
        import io
        import sys
        output_buffer = io.StringIO()
        sys.stdout = output_buffer
        
        # Execute code
        exec(code, namespace)
        
        # Restore stdout
        sys.stdout = sys.__stdout__
        
        output = output_buffer.getvalue()
        return f"✅ Code executed:\n{output}" if output else "✅ Code executed successfully (no output)"
        
    except Exception as e:
        import sys
        sys.stdout = sys.__stdout__
        return f"❌ Python execution error: {str(e)}"


def open_any_file(file_path: str) -> str:
    """
    Open any file with default application.
    
    Args:
        file_path: Path to file to open
        
    Returns:
        Success or error message
    """
    try:
        file_path = os.path.expanduser(file_path)
        
        if not os.path.exists(file_path):
            return f"❌ File not found: {file_path}"
        
        system = platform.system()
        
        if system == "Windows":
            os.startfile(file_path)
        elif system == "Darwin":  # macOS
            subprocess.run(["open", file_path])
        else:  # Linux
            subprocess.run(["xdg-open", file_path])
        
        return f"✅ Opened: {file_path}"
        
    except Exception as e:
        return f"❌ Failed to open file: {str(e)}"


def run_powershell(command: str) -> str:
    """
    Run PowerShell command on Windows.
    
    Args:
        command: PowerShell command
        
    Returns:
        Command output
    """
    if platform.system() != "Windows":
        return "❌ PowerShell only available on Windows"
    
    try:
        result = subprocess.run(
            ["powershell", "-Command", command],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        output = result.stdout if result.stdout else result.stderr
        return f"✅ PowerShell:\n{output}"
        
    except Exception as e:
        return f"❌ PowerShell error: {str(e)}"


def install_package(package_name: str) -> str:
    """
    Install Python package using pip.
    
    Args:
        package_name: Package to install
        
    Returns:
        Installation result
    """
    try:
        result = subprocess.run(
            [platform.sys.executable, "-m", "pip", "install", package_name],
            capture_output=True,
            text=True,
            timeout=120
        )
        
        if result.returncode == 0:
            return f"✅ Installed package: {package_name}"
        else:
            return f"❌ Failed to install {package_name}:\n{result.stderr}"
            
    except Exception as e:
        return f"❌ Installation error: {str(e)}"


def read_any_file(file_path: str, lines: int = None) -> str:
    """
    Read contents of any file.
    
    Args:
        file_path: Path to file
        lines: Number of lines to read (None = all)
        
    Returns:
        File contents
    """
    try:
        file_path = os.path.expanduser(file_path)
        
        if not os.path.exists(file_path):
            return f"❌ File not found: {file_path}"
        
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            if lines:
                content = ''.join(f.readlines()[:lines])
            else:
                content = f.read()
        
        return f"📄 {file_path}:\n{content}"
        
    except Exception as e:
        return f"❌ Failed to read file: {str(e)}"


def write_to_file(file_path: str, content: str, append: bool = False) -> str:
    """
    Write content to any file.
    
    Args:
        file_path: Path to file
        content: Content to write
        append: Append mode (default: overwrite)
        
    Returns:
        Success message
    """
    try:
        file_path = os.path.expanduser(file_path)
        mode = 'a' if append else 'w'
        
        with open(file_path, mode, encoding='utf-8') as f:
            f.write(content)
        
        action = "Appended to" if append else "Written to"
        return f"✅ {action}: {file_path}"
        
    except Exception as e:
        return f"❌ Failed to write file: {str(e)}"
