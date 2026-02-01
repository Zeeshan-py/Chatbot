"""
FRIDAY - AI-Powered Desktop Automation Assistant
Main entry point for the application.

Security Architecture:
1. AI (OpenAI) interprets user intent and returns structured JSON
2. Commands are validated against a whitelist
3. Only predefined, safe functions are executed
4. Risky operations require user confirmation
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from friday.ai_brain import ai_brain
from friday.command_parser import command_parser
from friday.config import config
from friday.utils import (
    print_header,
    print_info,
    print_success,
    print_error,
    print_warning,
    print_ai_response,
    print_divider,
    get_user_input,
    format_action_result,
    show_help,
    clear_screen
)


class FridayAssistant:
    """Main FRIDAY assistant controller"""
    
    def __init__(self):
        self.running = False
        self.ai = ai_brain
        self.parser = command_parser
    
    def start(self):
        """Start the FRIDAY assistant"""
        clear_screen()
        print_header()
        
        # Check configuration
        if config.openai_api_key:
            print_success("OpenAI API configured")
        else:
            print_warning("OpenAI API not configured - running in LOCAL MODE")
            print_info("Local mode uses pattern matching instead of AI")
        
        print_info("Type 'help' for available commands or 'exit' to quit")
        print_divider()
        
        self.running = True
        self.main_loop()
    
    def main_loop(self):
        """Main interaction loop"""
        while self.running:
            try:
                # Get user input
                user_input = get_user_input()
                
                if user_input is None:
                    # Handle Ctrl+C or EOF
                    self.shutdown()
                    break
                
                if not user_input:
                    continue
                
                # Handle special commands
                if self._handle_special_commands(user_input):
                    continue
                
                print_divider()
                
                # Process command through AI
                print_info("Processing your request...")
                command = self.ai.process_command(user_input)
                
                # Execute command
                exec_result = self.parser.parse_and_execute(command)
                
                # Display result
                if command["action"] == "chat":
                    response = command.get("parameters", {}).get("response", "")
                    print_ai_response(response)
                else:
                    if exec_result.get("success"):
                        print_success(exec_result.get("message", "Success"))
                    else:
                        print_error(exec_result.get("message", "Failed"))
                
                print_divider()
                
            except KeyboardInterrupt:
                print("\n")
                self.shutdown()
                break
            except Exception as e:
                print_error(f"Unexpected error: {str(e)}")
                print_divider()
    
    def _handle_special_commands(self, user_input: str) -> bool:
        """
        Handle special commands that don't need AI processing.
        
        Args:
            user_input: User's input
            
        Returns:
            True if command was handled, False otherwise
        """
        command = user_input.lower().strip()
        
        if command in ["exit", "quit", "bye", "goodbye"]:
            self.shutdown()
            return True
        
        elif command == "help":
            show_help()
            return True
        
        elif command == "clear":
            self.ai.clear_history()
            print_success("Conversation history cleared")
            return True
        
        elif command == "actions":
            actions = self.parser.get_available_actions()
            print_info("Available actions:")
            for action in actions:
                print(f"  • {action}")
            return True
        
        elif command == "cls" or command == "clear screen":
            clear_screen()
            print_header()
            return True
        
        elif command == "local mode":
            self.ai.use_local_mode = True
            print_success("Switched to LOCAL MODE (pattern matching)")
            return True
        
        elif command == "advanced mode on" or command == "enable advanced mode":
            self.parser.advanced_mode = True
            print_warning("⚠️  ADVANCED MODE ENABLED")
            print_warning("You now have broader system control!")
            print_warning("All advanced actions require confirmation.")
            print_info("New capabilities: execute_command, run_python, powershell, etc.")
            return True
        
        elif command == "advanced mode off" or command == "disable advanced mode":
            self.parser.advanced_mode = False
            print_success("Advanced mode disabled - back to safe mode")
            return True
        
        elif command == "mode" or command == "status":
            ai_mode = "AI Mode" if not self.ai.use_local_mode else "Local Mode"
            safety = "ADVANCED" if self.parser.advanced_mode else "SAFE"
            print_info(f"Current mode: {ai_mode}")
            print_info(f"Safety level: {safety}")
            if self.parser.advanced_mode:
                print_warning("⚠️  Advanced mode grants broader system access")
            return True
        
        elif command == "ai mode":
            if self.ai.openai_available:
                self.ai.use_local_mode = False
                print_success("Switched to AI MODE (OpenAI)")
            else:
                print_error("OpenAI is not available. Check your API key and quota.")
            return True
        
        elif command == "mode":
            mode = "LOCAL MODE" if self.ai.use_local_mode else "AI MODE"
            status = "✅ Active" if self.ai.openai_available else "❌ Unavailable"
            print_info(f"Current mode: {mode}")
            print_info(f"OpenAI status: {status}")
            return True
        
        return False
    
    def shutdown(self):
        """Shutdown FRIDAY gracefully"""
        print_divider()
        print_info("Shutting down FRIDAY...")
        print_success("Goodbye! 👋")
        self.running = False


def main():
    """Main entry point"""
    try:
        assistant = FridayAssistant()
        assistant.start()
    except Exception as e:
        print_error(f"Failed to start FRIDAY: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
