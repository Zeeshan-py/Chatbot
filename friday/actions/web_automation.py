"""
FRIDAY Web Automation Module - Super Powers!
Selenium-powered web browsing, reading, and interaction
Like Claude's computer use agent
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import json
from typing import Optional, Dict, Any


class WebAutomation:
    """Powerful web automation with Selenium"""
    
    def __init__(self):
        self.driver: Optional[webdriver.Chrome] = None
        self.wait: Optional[WebDriverWait] = None
        
    def start_browser(self, headless: bool = False) -> str:
        """
        Start Chrome browser with default profile.
        
        Args:
            headless: Run in background without window
            
        Returns:
            Success message
        """
        try:
            if self.driver:
                return "✅ Browser already running"
            
            options = Options()
            
            # Use default Chrome profile to avoid profile selection
            options.add_argument("--profile-directory=Default")
            options.add_argument("--disable-blink-features=AutomationControlled")
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)
            
            if headless:
                options.add_argument("--headless=new")
            
            # Initialize driver
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=options)
            self.wait = WebDriverWait(self.driver, 10)
            
            # Remove automation flags
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            return "✅ Chrome browser started (default profile)"
            
        except Exception as e:
            return f"❌ Failed to start browser: {str(e)}"
    
    def navigate_to(self, url: str) -> str:
        """
        Navigate to URL.
        
        Args:
            url: Website URL
            
        Returns:
            Success message
        """
        try:
            if not self.driver:
                self.start_browser()
            
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url
            
            self.driver.get(url)
            time.sleep(2)  # Wait for page load
            
            return f"✅ Navigated to {url}"
            
        except Exception as e:
            return f"❌ Navigation failed: {str(e)}"
    
    def google_search(self, query: str, open_first: bool = False) -> str:
        """
        Search on Google and optionally open first result.
        
        Args:
            query: Search query
            open_first: Open first search result
            
        Returns:
            Search results or success message
        """
        try:
            if not self.driver:
                self.start_browser()
            
            # Go to Google
            self.driver.get("https://www.google.com")
            time.sleep(1)
            
            # Find search box and enter query
            search_box = self.wait.until(
                EC.presence_of_element_located((By.NAME, "q"))
            )
            search_box.clear()
            search_box.send_keys(query)
            search_box.send_keys(Keys.RETURN)
            
            time.sleep(2)  # Wait for results
            
            if open_first:
                # Click first result
                try:
                    first_result = self.wait.until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, "h3"))
                    )
                    first_result.click()
                    time.sleep(2)
                    return f"✅ Searched '{query}' and opened first result"
                except:
                    pass
            
            return f"✅ Searched Google for '{query}'"
            
        except Exception as e:
            return f"❌ Search failed: {str(e)}"
    
    def read_page_content(self) -> str:
        """
        Read and extract text content from current page.
        
        Returns:
            Page content as text
        """
        try:
            if not self.driver:
                return "❌ Browser not started"
            
            # Get page source
            html = self.driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
            
            # Get text
            text = soup.get_text()
            
            # Clean up text
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = '\n'.join(chunk for chunk in chunks if chunk)
            
            # Limit to first 3000 characters
            if len(text) > 3000:
                text = text[:3000] + "\n... (content truncated)"
            
            title = self.driver.title
            url = self.driver.current_url
            
            return f"📄 Page: {title}\n🔗 URL: {url}\n\n{text}"
            
        except Exception as e:
            return f"❌ Failed to read page: {str(e)}"
    
    def extract_data(self, selector: str, attribute: str = None) -> str:
        """
        Extract specific data from page using CSS selector.
        
        Args:
            selector: CSS selector
            attribute: HTML attribute to extract (None = text content)
            
        Returns:
            Extracted data
        """
        try:
            if not self.driver:
                return "❌ Browser not started"
            
            elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
            
            if not elements:
                return f"❌ No elements found with selector: {selector}"
            
            results = []
            for elem in elements[:10]:  # Limit to 10 items
                if attribute:
                    value = elem.get_attribute(attribute)
                else:
                    value = elem.text
                
                if value:
                    results.append(value)
            
            return "✅ Extracted data:\n" + "\n".join(f"• {r}" for r in results)
            
        except Exception as e:
            return f"❌ Extraction failed: {str(e)}"
    
    def click_element(self, text: str = None, selector: str = None) -> str:
        """
        Click element by text or CSS selector.
        
        Args:
            text: Button/link text
            selector: CSS selector
            
        Returns:
            Success message
        """
        try:
            if not self.driver:
                return "❌ Browser not started"
            
            if text:
                # Find by text
                element = self.wait.until(
                    EC.element_to_be_clickable((By.XPATH, f"//*[contains(text(), '{text}')]"))
                )
            elif selector:
                # Find by selector
                element = self.wait.until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                )
            else:
                return "❌ Provide either text or selector"
            
            element.click()
            time.sleep(1)
            
            return f"✅ Clicked element"
            
        except Exception as e:
            return f"❌ Click failed: {str(e)}"
    
    def fill_form(self, field_selector: str, value: str) -> str:
        """
        Fill form field with value.
        
        Args:
            field_selector: CSS selector for input field
            value: Value to enter
            
        Returns:
            Success message
        """
        try:
            if not self.driver:
                return "❌ Browser not started"
            
            field = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, field_selector))
            )
            field.clear()
            field.send_keys(value)
            
            return f"✅ Filled field with: {value}"
            
        except Exception as e:
            return f"❌ Fill failed: {str(e)}"
    
    def take_page_screenshot(self, filename: str = None) -> str:
        """
        Take screenshot of current page.
        
        Args:
            filename: Screenshot filename (None = auto)
            
        Returns:
            Success message with file path
        """
        try:
            if not self.driver:
                return "❌ Browser not started"
            
            if not filename:
                from datetime import datetime
                filename = f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            
            if not filename.endswith('.png'):
                filename += '.png'
            
            import os
            desktop = os.path.join(os.path.expanduser('~'), 'Desktop')
            filepath = os.path.join(desktop, filename)
            
            self.driver.save_screenshot(filepath)
            
            return f"✅ Screenshot saved: {filepath}"
            
        except Exception as e:
            return f"❌ Screenshot failed: {str(e)}"
    
    def get_page_info(self) -> str:
        """
        Get current page information.
        
        Returns:
            Page title, URL, and summary
        """
        try:
            if not self.driver:
                return "❌ Browser not started"
            
            title = self.driver.title
            url = self.driver.current_url
            
            # Get headings
            h1_elements = self.driver.find_elements(By.TAG_NAME, "h1")
            h1_text = [h.text for h in h1_elements[:3] if h.text]
            
            info = f"📄 Page: {title}\n"
            info += f"🔗 URL: {url}\n"
            
            if h1_text:
                info += f"📌 Main headings:\n"
                info += "\n".join(f"  • {h}" for h in h1_text)
            
            return info
            
        except Exception as e:
            return f"❌ Failed to get page info: {str(e)}"
    
    def scroll_page(self, direction: str = "down") -> str:
        """
        Scroll page up or down.
        
        Args:
            direction: 'up' or 'down'
            
        Returns:
            Success message
        """
        try:
            if not self.driver:
                return "❌ Browser not started"
            
            if direction.lower() == "down":
                self.driver.execute_script("window.scrollBy(0, 500);")
            else:
                self.driver.execute_script("window.scrollBy(0, -500);")
            
            return f"✅ Scrolled {direction}"
            
        except Exception as e:
            return f"❌ Scroll failed: {str(e)}"
    
    def go_back(self) -> str:
        """Go back to previous page"""
        try:
            if not self.driver:
                return "❌ Browser not started"
            
            self.driver.back()
            time.sleep(1)
            return "✅ Navigated back"
            
        except Exception as e:
            return f"❌ Failed: {str(e)}"
    
    def close_browser(self) -> str:
        """Close the browser"""
        try:
            if self.driver:
                self.driver.quit()
                self.driver = None
                self.wait = None
                return "✅ Browser closed"
            return "ℹ️  Browser not running"
            
        except Exception as e:
            return f"❌ Failed to close: {str(e)}"


# Global instance
web_automation = WebAutomation()


# Convenience functions for command parser
def start_browser(headless: bool = False) -> str:
    """Start web browser"""
    return web_automation.start_browser(headless)


def browse_to(url: str) -> str:
    """Navigate to URL"""
    return web_automation.navigate_to(url)


def search_and_browse(query: str, open_result: bool = True) -> str:
    """Search Google and optionally open first result"""
    return web_automation.google_search(query, open_result)


def read_webpage() -> str:
    """Read current webpage content"""
    return web_automation.read_page_content()


def get_webpage_info() -> str:
    """Get current page info"""
    return web_automation.get_page_info()


def close_browser() -> str:
    """Close browser"""
    return web_automation.close_browser()


def webpage_screenshot(filename: str = None) -> str:
    """Take webpage screenshot"""
    return web_automation.take_page_screenshot(filename)
