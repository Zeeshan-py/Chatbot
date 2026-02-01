"""
FRIDAY System Control Module
Handles system information and safe system operations.
"""

import platform
import psutil
import requests
from typing import Optional
from datetime import datetime
from friday.config import config


def get_news(category: str = "general") -> str:
    """
    Fetch latest news headlines.
    
    Args:
        category: News category (general, business, technology, etc.)
        
    Returns:
        Formatted news headlines or error message
    """
    try:
        api_key = config.news_api_key
        
        if not api_key:
            return "⚠️  News API key not configured. Please add NEWS_API_KEY to .env.json"
        
        # Fetch news
        url = f"https://newsapi.org/v2/top-headlines"
        params = {
            "country": "us",
            "category": category,
            "apiKey": api_key,
            "pageSize": 5
        }
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        
        news_data = response.json()
        
        if news_data.get("status") == "ok":
            articles = news_data.get("articles", [])
            
            if not articles:
                return "⚠️  No news articles found"
            
            # Format news
            result = [f"📰 Top {category.capitalize()} News:\n"]
            
            for i, article in enumerate(articles, 1):
                title = article.get("title", "No title")
                source = article.get("source", {}).get("name", "Unknown")
                result.append(f"{i}. {title}")
                result.append(f"   Source: {source}\n")
            
            return "\n".join(result)
        else:
            return f"❌ News API error: {news_data.get('message', 'Unknown error')}"
            
    except requests.exceptions.RequestException as e:
        return f"❌ Failed to fetch news: {str(e)}"
    except Exception as e:
        return f"❌ Error: {str(e)}"


def get_system_info() -> str:
    """
    Get system information.
    
    Returns:
        Formatted system information
    """
    try:
        info = []
        
        # Basic info
        info.append("💻 System Information:")
        info.append(f"OS: {platform.system()} {platform.release()}")
        info.append(f"Machine: {platform.machine()}")
        info.append(f"Processor: {platform.processor()}")
        
        # CPU info
        cpu_percent = psutil.cpu_percent(interval=1)
        cpu_count = psutil.cpu_count()
        info.append(f"\n🔥 CPU: {cpu_count} cores, {cpu_percent}% usage")
        
        # Memory info
        memory = psutil.virtual_memory()
        memory_gb = memory.total / (1024 ** 3)
        memory_used_gb = memory.used / (1024 ** 3)
        info.append(f"💾 RAM: {memory_used_gb:.1f}GB / {memory_gb:.1f}GB ({memory.percent}%)")
        
        # Disk info
        disk = psutil.disk_usage('/')
        disk_total_gb = disk.total / (1024 ** 3)
        disk_used_gb = disk.used / (1024 ** 3)
        info.append(f"💿 Disk: {disk_used_gb:.1f}GB / {disk_total_gb:.1f}GB ({disk.percent}%)")
        
        return "\n".join(info)
        
    except Exception as e:
        return f"❌ Failed to get system info: {str(e)}"


def get_time() -> str:
    """
    Get current date and time.
    
    Returns:
        Formatted current date and time
    """
    try:
        now = datetime.now()
        date_str = now.strftime("%A, %B %d, %Y")
        time_str = now.strftime("%I:%M:%S %p")
        
        return f"📅 {date_str}\n🕐 {time_str}"
        
    except Exception as e:
        return f"❌ Failed to get time: {str(e)}"


def get_battery_status() -> str:
    """
    Get battery status (for laptops).
    
    Returns:
        Battery information or message if not available
    """
    try:
        battery = psutil.sensors_battery()
        
        if battery is None:
            return "🔌 No battery detected (desktop computer)"
        
        percent = battery.percent
        plugged = battery.power_plugged
        
        status = "Charging" if plugged else "Discharging"
        
        result = f"🔋 Battery: {percent}% ({status})"
        
        if not plugged and battery.secsleft > 0:
            hours = battery.secsleft // 3600
            minutes = (battery.secsleft % 3600) // 60
            result += f"\n⏱️  Time remaining: {hours}h {minutes}m"
        
        return result
        
    except Exception as e:
        return f"❌ Failed to get battery status: {str(e)}"


def list_running_processes() -> str:
    """
    List currently running processes.
    
    Returns:
        List of top processes by CPU usage
    """
    try:
        processes = []
        
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent']):
            try:
                processes.append(proc.info)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        
        # Sort by CPU usage
        processes.sort(key=lambda x: x['cpu_percent'] or 0, reverse=True)
        
        # Top 10 processes
        result = ["🔄 Top Processes by CPU Usage:\n"]
        
        for i, proc in enumerate(processes[:10], 1):
            name = proc['name']
            pid = proc['pid']
            cpu = proc['cpu_percent'] or 0
            result.append(f"{i}. {name} (PID: {pid}) - {cpu:.1f}% CPU")
        
        return "\n".join(result)
        
    except Exception as e:
        return f"❌ Failed to list processes: {str(e)}"


# Note: Dangerous system operations (shutdown, restart) are intentionally NOT implemented
# These would require additional safety measures and user confirmation
