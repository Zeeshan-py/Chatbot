"""
FRIDAY - AI-Powered Desktop Automation Assistant
Main entry point for the application.
"""

import sys
import io

# Force UTF-8 encoding for stdout and stderr to handle emojis on Windows
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')
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
            print_success("OpenAI API configured - AGENT MODE ACTIVE")
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
                
                # Handle special commands (exit, help, etc.)
                if self._handle_special_commands(user_input):
                    continue
                
                print_divider()
                
                # Process command through AI
                print_info("Thinking...")
                
                # The Brain now handles the Agentic Loop (Think -> Tool -> Action -> Think)
                # It returns the final response as a "chat" action
                command = self.ai.process_command(user_input)
                
                # In the new architecture, the brain executes tools internally.
                # We mainly look for the final response.
                if command["action"] == "chat":
                    response = command.get("parameters", {}).get("response", "")
                    print_ai_response(response)
                else:
                    # Fallback for local mode or legacy responses
                    exec_result = self.parser.parse_and_execute(command)
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
        """
        command = user_input.lower().strip()
        
        if command in ["exit", "quit", "bye", "goodbye"]:
            self.shutdown()
            return True
        
        elif command == "help":
            show_help()
            return True
        
        elif command == "clear" or command == "cls":
            clear_screen()
            print_header()
            return True
        
        elif command == "reset":
            self.ai.conversation_history = []
            print_success("Conversation history cleared")
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
