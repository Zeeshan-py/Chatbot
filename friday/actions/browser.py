"""
FRIDAY Browser Control Module
Powered by Selenium for full web automation capabilities.
"""

import webbrowser
import urllib.parse
from friday.config import SEARCH_ENGINES


def search_web(query: str, engine: str = "google") -> str:
    """
    Search the web using Selenium browser automation.
    Opens browser, searches, and can read results.
    
    Args:
        query: Search query
        engine: Search engine to use (google, bing, duckduckgo, youtube)
        
    Returns:
        Success or error message
    """
    try:
        from friday.actions.web_automation import web_automation
        
        # Start browser if not running
        if not web_automation.driver:
            web_automation.start_browser()
        
        engine_lower = engine.lower()
        
        if engine_lower == "google" or engine_lower not in SEARCH_ENGINES:
            return web_automation.google_search(query, open_first=False)
        elif engine_lower == "youtube":
            encoded = urllib.parse.quote(query)
            web_automation.navigate_to(f"https://www.youtube.com/results?search_query={encoded}")
            return f"✅ Searched YouTube for '{query}'"
        elif engine_lower == "bing":
            encoded = urllib.parse.quote(query)
            web_automation.navigate_to(f"https://www.bing.com/search?q={encoded}")
            return f"✅ Searched Bing for '{query}'"
        else:
            # Fallback to Google
            return web_automation.google_search(query, open_first=False)
        
    except Exception as e:
        return f"❌ Failed to search: {str(e)}"


def open_url(url: str) -> str:
    """
    Open URL in Selenium-controlled browser with full automation.
    
    Args:
        url: URL to open
        
    Returns:
        Success or error message
    """
    try:
        from friday.actions.web_automation import web_automation
        
        # Start browser if not running
        if not web_automation.driver:
            web_automation.start_browser()
        
        # Add protocol if missing
        if not url.startswith(("http://", "https://")):
            url = "https://" + url
        
        result = web_automation.navigate_to(url)
        return result
        
    except Exception as e:
        return f"❌ Failed to open URL: {str(e)}"
