"""
FRIDAY Configuration Module
Manages API keys, settings, and environment variables securely.
"""

import os
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv


class Config:
    """Configuration manager for FRIDAY assistant"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        
        # Load .env file
        env_path = self.project_root / ".env"
        load_dotenv(dotenv_path=env_path)
        
        self._openai_api_key: Optional[str] = None
        self._news_api_key: Optional[str] = None
        
        # Load configuration
        self._load_config()
    
    def _load_config(self) -> None:
        """Load configuration from environment variables"""
        self._openai_api_key = os.getenv('OPENAI_API_KEY')
        self._news_api_key = os.getenv('NEWS_API_KEY')
    
    @property
    def openai_api_key(self) -> Optional[str]:
        """Get OpenAI API key (returns None if not configured)"""
        return self._openai_api_key
    
    @property
    def news_api_key(self) -> Optional[str]:
        """Get News API key (optional)"""
        return self._news_api_key
    
    def create_config_template(self) -> None:
        """Create a template .env file"""
        env_example_path = self.project_root / ".env.example"
        env_path = self.project_root / ".env"
        
        template = """# Environment Variables for FRIDAY Assistant
# IMPORTANT: Never commit this file to GitHub!

# OpenAI API Key - Get from https://platform.openai.com/api-keys
OPENAI_API_KEY=your-openai-api-key-here

# News API Key - Get from https://newsapi.org (Optional)
NEWS_API_KEY=your-news-api-key-here
"""
        
        if not env_path.exists():
            with open(env_path, 'w') as f:
                f.write(template)
            print(f"Created .env file at: {env_path}")
            print("Please add your API keys to this file.")
        else:
            print(f".env file already exists at: {env_path}")
        
        # Always create/update .env.example for GitHub
        if not env_example_path.exists():
            with open(env_example_path, 'w') as f:
                f.write(template)
            print(f"Created .env.example template at: {env_example_path}")


# Global config instance
config = Config()


# Safety settings
SAFETY_SETTINGS = {
    "require_confirmation_for": [
        "delete_file",
        "delete_folder",
        "move_multiple_files",
        "organize_downloads",
        "close_app",
        "shutdown_system",
        "restart_system"
    ],
    "blocked_paths": [
        "C:\\Windows",
        "C:\\Program Files",
        "C:\\Program Files (x86)",
        "/System",
        "/usr/bin",
        "/bin",
        "/sbin"
    ],
    "max_files_without_confirmation": 5
}


# Application mappings for common names
APP_MAPPINGS = {
    "chrome": ["chrome", "google chrome"],
    "firefox": ["firefox", "mozilla firefox"],
    "edge": ["msedge", "microsoft edge", "edge"],
    "notepad": ["notepad"],
    "calculator": ["calc", "calculator"],
    "explorer": ["explorer", "file explorer"],
    "vscode": ["code", "visual studio code", "vs code"],
    "cmd": ["cmd", "command prompt"],
    "powershell": ["powershell", "pwsh"],
    "paint": ["mspaint", "paint"],
    "word": ["winword", "microsoft word", "word"],
    "excel": ["excel", "microsoft excel"],
    "spotify": ["spotify"],
    "discord": ["discord"],
    "slack": ["slack"],
    "whatsapp": ["whatsapp"],
    "settings": ["ms-settings:", "settings", "setting"],
    "camera": ["microsoft.windows.camera:", "camera"],
    "photos": ["microsoft.windows.photos:", "photos"],
    "store": ["ms-windows-store:", "store", "microsoft store"],
}


# Web search engines
SEARCH_ENGINES = {
    "google": "https://www.google.com/search?q={}",
    "bing": "https://www.bing.com/search?q={}",
    "duckduckgo": "https://duckduckgo.com/?q={}",
    "youtube": "https://www.youtube.com/results?search_query={}"
}

# Website Shortcuts for Natural Language
WEBSITE_MAPPINGS = {
    "yt": "youtube.com",
    "youtube": "youtube.com",
    "fb": "facebook.com",
    "facebook": "facebook.com",
    "ig": "instagram.com",
    "instagram": "instagram.com",
    "twitter": "twitter.com",
    "x": "x.com",
    "github": "github.com",
    "git": "github.com",
    "google": "google.com",
    "gpt": "chatgpt.com",
    "chatgpt": "chatgpt.com",
    "gmail": "gmail.com",
    "mail": "gmail.com",
    "amazon": "amazon.com",
    "reddit": "reddit.com",
    "netflix": "netflix.com",
    "linkedin": "linkedin.com",
    "whatsapp": "web.whatsapp.com", # distinguish from app
}
