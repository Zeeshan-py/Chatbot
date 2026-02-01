"""
FRIDAY Mouse and Keyboard Control Module
Handles mouse movements, clicks, keyboard input, and screenshots.
"""

import pyautogui
from pathlib import Path
from typing import Optional


# Set safety features
pyautogui.FAILSAFE = True  # Move mouse to corner to abort
pyautogui.PAUSE = 0.1  # Small pause between actions


def mouse_click(x: Optional[int] = None, y: Optional[int] = None, button: str = "left") -> str:
    """
    Click mouse at specified coordinates or current position.
    
    Args:
        x: X coordinate (optional)
        y: Y coordinate (optional)
        button: Mouse button ('left', 'right', 'middle')
        
    Returns:
        Success or error message
    """
    try:
        button_lower = button.lower()
        
        if button_lower not in ["left", "right", "middle"]:
            return f"❌ Invalid button: {button}. Use 'left', 'right', or 'middle'"
        
        if x is not None and y is not None:
            # Validate coordinates
            screen_width, screen_height = pyautogui.size()
            if x < 0 or x > screen_width or y < 0 or y > screen_height:
                return f"❌ Coordinates out of range. Screen size: {screen_width}x{screen_height}"
            
            pyautogui.click(x, y, button=button_lower)
            return f"✅ Clicked {button} button at ({x}, {y})"
        else:
            pyautogui.click(button=button_lower)
            return f"✅ Clicked {button} button at current position"
            
    except Exception as e:
        return f"❌ Failed to click: {str(e)}"


def mouse_move(x: int, y: int, duration: float = 0.5) -> str:
    """
    Move mouse to specified coordinates.
    
    Args:
        x: X coordinate
        y: Y coordinate
        duration: Time to move (seconds)
        
    Returns:
        Success or error message
    """
    try:
        # Validate coordinates
        screen_width, screen_height = pyautogui.size()
        if x < 0 or x > screen_width or y < 0 or y > screen_height:
            return f"❌ Coordinates out of range. Screen size: {screen_width}x{screen_height}"
        
        pyautogui.moveTo(x, y, duration=duration)
        return f"✅ Moved mouse to ({x}, {y})"
        
    except Exception as e:
        return f"❌ Failed to move mouse: {str(e)}"


def type_text(text: str, interval: float = 0.05) -> str:
    """
    Type text using keyboard.
    
    Args:
        text: Text to type
        interval: Delay between keystrokes (seconds)
        
    Returns:
        Success or error message
    """
    try:
        pyautogui.write(text, interval=interval)
        
        # Truncate display for long text
        display_text = text if len(text) <= 50 else text[:50] + "..."
        return f"✅ Typed: {display_text}"
        
    except Exception as e:
        return f"❌ Failed to type text: {str(e)}"


def press_key(key: str, presses: int = 1) -> str:
    """
    Press a keyboard key.
    
    Args:
        key: Key to press (e.g., 'enter', 'space', 'ctrl', 'alt', 'tab')
        presses: Number of times to press
        
    Returns:
        Success or error message
    """
    try:
        # Validate key
        valid_keys = pyautogui.KEYBOARD_KEYS
        key_lower = key.lower()
        
        if key_lower not in valid_keys:
            return f"❌ Invalid key: {key}. Use pyautogui key names."
        
        pyautogui.press(key_lower, presses=presses)
        
        press_text = "time" if presses == 1 else "times"
        return f"✅ Pressed '{key}' {presses} {press_text}"
        
    except Exception as e:
        return f"❌ Failed to press key: {str(e)}"


def take_screenshot(save_path: Optional[str] = None) -> str:
    """
    Take a screenshot and save it.
    
    Args:
        save_path: Path to save screenshot (optional)
        
    Returns:
        Success or error message with file path
    """
    try:
        # Default path if not provided
        if save_path is None:
            screenshots_dir = Path.home() / "Pictures" / "Screenshots"
            screenshots_dir.mkdir(parents=True, exist_ok=True)
            
            # Generate filename with timestamp
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            save_path = str(screenshots_dir / f"screenshot_{timestamp}.png")
        
        # Take screenshot
        screenshot = pyautogui.screenshot()
        
        # Save
        path = Path(save_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        screenshot.save(str(path))
        
        return f"✅ Screenshot saved: {path.absolute()}"
        
    except Exception as e:
        return f"❌ Failed to take screenshot: {str(e)}"


def get_mouse_position() -> str:
    """
    Get current mouse position.
    
    Returns:
        Current mouse coordinates
    """
    try:
        x, y = pyautogui.position()
        screen_width, screen_height = pyautogui.size()
        
        return f"🖱️  Mouse position: ({x}, {y})\n📺 Screen size: {screen_width}x{screen_height}"
        
    except Exception as e:
        return f"❌ Failed to get mouse position: {str(e)}"


def get_screen_size() -> str:
    """
    Get screen resolution.
    
    Returns:
        Screen dimensions
    """
    try:
        width, height = pyautogui.size()
        return f"📺 Screen size: {width}x{height}"
        
    except Exception as e:
        return f"❌ Failed to get screen size: {str(e)}"
