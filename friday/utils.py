"""
FRIDAY Utility Functions
Helper functions used across the application.
"""

import sys
from typing import Optional
from colorama import init, Fore, Style


# Initialize colorama for colored terminal output
init(autoreset=True)


def print_header():
    """Print FRIDAY welcome header"""
    header = f"""
{Fore.CYAN}╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║  {Fore.YELLOW}███████╗██████╗ ██╗██████╗  █████╗ ██╗   ██╗{Fore.CYAN}                ║
║  {Fore.YELLOW}██╔════╝██╔══██╗██║██╔══██╗██╔══██╗╚██╗ ██╔╝{Fore.CYAN}                ║
║  {Fore.YELLOW}█████╗  ██████╔╝██║██║  ██║███████║ ╚████╔╝{Fore.CYAN}                 ║
║  {Fore.YELLOW}██╔══╝  ██╔══██╗██║██║  ██║██╔══██║  ╚██╔╝{Fore.CYAN}                  ║
║  {Fore.YELLOW}██║     ██║  ██║██║██████╔╝██║  ██║   ██║{Fore.CYAN}                   ║
║  {Fore.YELLOW}╚═╝     ╚═╝  ╚═╝╚═╝╚═════╝ ╚═╝  ╚═╝   ╚═╝{Fore.CYAN}                   ║
║                                                              ║
║          {Fore.GREEN}AI-Powered Desktop Automation Assistant{Fore.CYAN}              ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
{Style.RESET_ALL}"""
    print(header)


def print_info(message: str):
    """Print info message in blue"""
    print(f"{Fore.BLUE}ℹ️  {message}{Style.RESET_ALL}")


def print_success(message: str):
    """Print success message in green"""
    print(f"{Fore.GREEN}✅ {message}{Style.RESET_ALL}")


def print_error(message: str):
    """Print error message in red"""
    print(f"{Fore.RED}❌ {message}{Style.RESET_ALL}")


def print_warning(message: str):
    """Print warning message in yellow"""
    print(f"{Fore.YELLOW}⚠️  {message}{Style.RESET_ALL}")


def print_ai_response(message: str):
    """Print AI response with special formatting"""
    print(f"{Fore.MAGENTA}🤖 FRIDAY: {Fore.WHITE}{message}{Style.RESET_ALL}")


def print_divider():
    """Print a divider line"""
    print(f"{Fore.CYAN}{'─' * 64}{Style.RESET_ALL}")


def get_user_input(prompt: str = "You") -> Optional[str]:
    """
    Get user input with formatted prompt.
    
    Args:
        prompt: Prompt text to display
        
    Returns:
        User input string or None if interrupted
    """
    try:
        user_input = input(f"{Fore.CYAN}👤 {prompt}: {Style.RESET_ALL}").strip()
        return user_input
    except KeyboardInterrupt:
        print("\n")
        return None
    except EOFError:
        return None


def confirm_action(prompt: str) -> bool:
    """
    Ask user for yes/no confirmation.
    
    Args:
        prompt: Question to ask
        
    Returns:
        True if user confirms, False otherwise
    """
    try:
        response = input(f"{Fore.YELLOW}⚠️  {prompt} (yes/no): {Style.RESET_ALL}").strip().lower()
        return response in ["yes", "y"]
    except (KeyboardInterrupt, EOFError):
        return False


def format_action_result(result: str) -> str:
    """
    Format action result with appropriate colors.
    
    Args:
        result: Result message from action execution
        
    Returns:
        Formatted result string
    """
    if result.startswith("✅"):
        return f"{Fore.GREEN}{result}{Style.RESET_ALL}"
    elif result.startswith("❌"):
        return f"{Fore.RED}{result}{Style.RESET_ALL}"
    elif result.startswith("⚠️"):
        return f"{Fore.YELLOW}{result}{Style.RESET_ALL}"
    elif result.startswith("📰") or result.startswith("💻") or result.startswith("🔋"):
        return f"{Fore.CYAN}{result}{Style.RESET_ALL}"
    else:
        return result


def show_help():
    """Show help information"""
    help_text = f"""
{Fore.CYAN}╔══════════════════════════════════════════════════════════════╗
║                      FRIDAY HELP                             ║
╚══════════════════════════════════════════════════════════════╝{Style.RESET_ALL}

{Fore.YELLOW}Available Commands:{Style.RESET_ALL}

{Fore.RED}⚠️  IMPORTANT: Type commands WITHOUT quotes!{Style.RESET_ALL}
  ✅ Correct:   open chrome
  ❌ Wrong:     "open chrome"

{Fore.GREEN}Application Control:{Style.RESET_ALL}
  • Open Chrome/Firefox/Edge/Notepad
  • Close Chrome
  • Open VS Code

{Fore.GREEN}Web Browsing:{Style.RESET_ALL}
  • Search for Python tutorials
  • Open youtube.com
  • Go to github.com

{Fore.GREEN}File Management:{Style.RESET_ALL}
  • Create a file called test.txt
  • Create a folder called Projects
  • List files in Downloads
  • Organize my downloads folder
  • Delete file test.txt
  • Move file.txt to Documents

{Fore.GREEN}Mouse & Keyboard:{Style.RESET_ALL}
  • Click at 500, 300
  • Move mouse to 800, 600
  • Type Hello World
  • Press enter
  • Take a screenshot

{Fore.GREEN}System Information:{Style.RESET_ALL}
  • Get system info
  • What time is it?
  • Check battery status
  • Show running processes
  • Get the news

{Fore.GREEN}Special Commands:{Style.RESET_ALL}
  • help - Show this help message
  • clear - Clear conversation history
  • mode - Check current mode (AI or Local)
  • local mode - Switch to local pattern matching
  • ai mode - Switch to OpenAI (if available)
  • actions - List all available actions
  • exit/quit - Exit FRIDAY

{Fore.YELLOW}Note:{Style.RESET_ALL}
  • LOCAL MODE uses pattern matching (works without OpenAI)
  • AI MODE uses OpenAI for better understanding (requires API credits)
  • FRIDAY automatically switches to local mode if OpenAI quota is exceeded

{Fore.CYAN}╚══════════════════════════════════════════════════════════════╝{Style.RESET_ALL}
"""
    print(help_text)


def clear_screen():
    """Clear the terminal screen"""
    import os
    os.system('cls' if sys.platform == 'win32' else 'clear')
