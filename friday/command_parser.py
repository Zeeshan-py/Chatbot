"""
FRIDAY Command Parser Module
Validates AI-generated commands and routes them to safe, whitelisted functions.
Now includes ADVANCED MODE for broader system control.
"""

from typing import Dict, Any, Callable, Optional
from friday.actions import apps, files, browser, system, mouse_keyboard, advanced, web_automation
from friday.config import SAFETY_SETTINGS


class CommandParser:
    """
    Validates and routes AI commands to whitelisted functions.
    Implements security checks and user confirmation for risky operations.
    
    Modes:
    - SAFE MODE: Whitelisted commands only
    - ADVANCED MODE: Allows system commands and broader control
    """
    
    def __init__(self):
        self.advanced_mode = False  # Start in safe mode
        
        # Whitelist of allowed actions mapped to their implementation functions
        self.ALLOWED_ACTIONS: Dict[str, Callable] = {
            # Application control
            "open_app": apps.open_application,
            "close_app": apps.close_application,
            
            # Web and browser
            "search_web": browser.search_web,
            "open_url": browser.open_url,
            
            # File operations
            "create_file": files.create_file,
            "create_folder": files.create_folder,
            "delete_file": files.delete_file,
            "delete_folder": files.delete_folder,
            "move_file": files.move_file,
            "copy_file": files.copy_file,
            "list_files": files.list_files,
            "organize_downloads": files.organize_downloads,
            
            # Mouse and keyboard
            "mouse_click": mouse_keyboard.mouse_click,
            "mouse_move": mouse_keyboard.mouse_move,
            "type_text": mouse_keyboard.type_text,
            "press_key": mouse_keyboard.press_key,
            "take_screenshot": mouse_keyboard.take_screenshot,
            
            # System
            "get_news": system.get_news,
            
            # Web Automation - SUPER POWERS!
            "start_browser": web_automation.start_browser,
            "browse_to": web_automation.browse_to,
            "search_and_browse": web_automation.search_and_browse,
            "read_webpage": web_automation.read_webpage,
            "get_webpage_info": web_automation.get_webpage_info,
            "close_browser": web_automation.close_browser,
            "webpage_screenshot": web_automation.webpage_screenshot,
            "google_search": web_automation.google_search,
            
            # Advanced Mode Actions (⚠️ powerful!)
            "execute_command": advanced.execute_system_command,
            "run_python": advanced.run_python_code,
            "open_file": advanced.open_any_file,
            "powershell": advanced.run_powershell,
            "install_package": advanced.install_package,
            "read_file": advanced.read_any_file,
            "write_file": advanced.write_to_file,
            
            # Chat (no action)
            "chat": self._handle_chat,
        }
        
        self.actions_requiring_confirmation = set(
            SAFETY_SETTINGS["require_confirmation_for"]
        )
        
        # Advanced mode actions ALWAYS require confirmation
        self.advanced_actions = {
            "execute_command", "run_python", "powershell", 
            "write_file", "install_package"
        }
    
    def parse_and_execute(self, command: Dict[str, Any], auto_confirm: bool = False) -> Dict[str, Any]:
        """
        Parse AI command, validate it, and execute the corresponding function.
        
        Args:
            command: Dictionary with 'action', 'parameters', and 'reasoning'
            auto_confirm: If True, skip user confirmation (for automated testing)
            
        Returns:
            Dictionary with 'success', 'message', and optional 'data'
        """
        action = command.get("action")
        parameters = command.get("parameters", {})
        reasoning = command.get("reasoning", "")
        
        # Validate action is in whitelist
        if action not in self.ALLOWED_ACTIONS:
            return {
                "success": False,
                "message": f"Security Error: Action '{action}' is not whitelisted."
            }
        
        # Check if advanced mode required
        if action in self.advanced_actions and not self.advanced_mode:
            return {
                "success": False,
                "message": f"⚠️ '{action}' requires ADVANCED MODE. Enable with 'advanced mode on'"
            }
        
        # Display reasoning
        if reasoning:
            print(f"\n💭 FRIDAY's reasoning: {reasoning}")
        
        # Check if confirmation is required
        needs_confirm = (action in self.actions_requiring_confirmation or 
                        action in self.advanced_actions)
        
        if needs_confirm and not auto_confirm:
            if not self._get_user_confirmation(action, parameters):
                return {
                    "success": False,
                    "message": "Action cancelled by user."
                }
        
        # Execute the whitelisted function
        try:
            function = self.ALLOWED_ACTIONS[action]
            result = function(**parameters)
            return {
                "success": True,
                "message": result if isinstance(result, str) else "Action completed successfully",
                "data": result if not isinstance(result, str) else None
            }
        except TypeError as e:
            return {
                "success": False,
                "message": f"Invalid parameters for action '{action}': {str(e)}"
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Error executing '{action}': {str(e)}"
            }
    
    def _get_user_confirmation(self, action: str, parameters: Dict[str, Any]) -> bool:
        """
        Ask user for confirmation before executing risky actions.
        
        Args:
            action: The action to be performed
            parameters: Parameters for the action
            
        Returns:
            True if user confirms, False otherwise
        """
        print(f"\n⚠️  CONFIRMATION REQUIRED")
        print(f"Action: {action}")
        print(f"Parameters: {parameters}")
        
        response = input("\nDo you want to proceed? (yes/no): ").strip().lower()
        
        return response in ["yes", "y"]
    
    def _handle_chat(self, response: str) -> str:
        """
        Handle chat-only responses (no action needed).
        
        Args:
            response: The chat response from AI
            
        Returns:
            The response string
        """
        return response
    
    def is_action_allowed(self, action: str) -> bool:
        """Check if an action is in the whitelist"""
        return action in self.ALLOWED_ACTIONS
    
    def get_available_actions(self) -> list:
        """Get list of all available actions"""
        return list(self.ALLOWED_ACTIONS.keys())


# Global command parser instance
command_parser = CommandParser()
