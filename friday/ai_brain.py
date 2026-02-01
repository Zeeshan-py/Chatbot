"""
FRIDAY AI Brain Module
Handles communication with OpenAI API and ensures structured JSON responses.
Includes local fallback for when OpenAI is unavailable.
"""

import json
import re
from typing import Dict, Any, Optional
from openai import OpenAI
from friday.config import config


class AIBrain:
    """
    AI Brain that communicates with OpenAI to interpret user intent
    and return structured JSON commands.
    """
    
    def __init__(self):
        try:
            self.client = OpenAI(api_key=config.openai_api_key)
            self.model = "gpt-3.5-turbo"
            self.openai_available = True
        except Exception:
            self.client = None
            self.openai_available = False
        
        self.conversation_history = []
        self.use_local_mode = not self.openai_available
        
    def _get_system_prompt(self) -> str:
        """
        System prompt that instructs the AI to return structured JSON commands
        and follow strict safety guidelines.
        """
        return """You are FRIDAY, an AI-powered desktop automation assistant.

CRITICAL RULES:
1. You MUST respond ONLY in valid JSON format
2. You can ONLY use actions from the ALLOWED_ACTIONS list
3. NEVER invent new actions or commands
4. If you cannot perform a task safely, use the "chat" action to explain why
5. Always be concise and helpful

ALLOWED_ACTIONS:
- open_app: Open an application (parameters: app_name)
- close_app: Close an application (parameters: app_name)
- search_web: Search on the web (parameters: query, engine)
- open_url: Open a specific URL (parameters: url)
- create_file: Create a new file (parameters: file_path, content)
- create_folder: Create a new folder (parameters: folder_path)
- delete_file: Delete a file (parameters: file_path)
- delete_folder: Delete a folder (parameters: folder_path)
- move_file: Move a file (parameters: source, destination)
- copy_file: Copy a file (parameters: source, destination)
- list_files: List files in a directory (parameters: directory_path)
- organize_downloads: Organize downloads folder by file type (parameters: none)
- mouse_click: Click at coordinates (parameters: x, y, button)
- mouse_move: Move mouse to coordinates (parameters: x, y)
- type_text: Type text (parameters: text)
- press_key: Press a keyboard key (parameters: key)
- take_screenshot: Take a screenshot (parameters: save_path)
- get_news: Fetch latest news (parameters: category)
- chat: Just chat without action (parameters: response)

RESPONSE FORMAT:
Always respond with valid JSON in this exact format:

{
  "action": "action_name",
  "parameters": {
    "param1": "value1",
    "param2": "value2"
  },
  "reasoning": "Brief explanation of why you chose this action"
}

For chat responses:
{
  "action": "chat",
  "parameters": {
    "response": "Your message here"
  },
  "reasoning": "User asked a question that doesn't require automation"
}

EXAMPLES:

User: "Open Chrome"
Response:
{
  "action": "open_app",
  "parameters": {
    "app_name": "chrome"
  },
  "reasoning": "User wants to launch Google Chrome browser"
}

User: "Search for Python tutorials"
Response:
{
  "action": "search_web",
  "parameters": {
    "query": "Python tutorials",
    "engine": "google"
  },
  "reasoning": "User wants to search for educational content"
}

User: "What's the weather like?"
Response:
{
  "action": "chat",
  "parameters": {
    "response": "I can't check the weather directly, but I can search for it online. Would you like me to search for your local weather?"
  },
  "reasoning": "Weather checking requires external API not in allowed actions"
}

User: "Create a folder called Projects"
Response:
{
  "action": "create_folder",
  "parameters": {
    "folder_path": "Projects"
  },
  "reasoning": "User wants to create a new directory"
}

SAFETY RULES:
- Never suggest actions that could harm the system
- If unsure about a path, ask for clarification
- Always use relative paths unless absolute paths are explicitly provided
- For destructive actions (delete, move), be explicit about what will happen
- If the user's request is ambiguous, ask for clarification using "chat" action

Remember: ONLY output valid JSON. No additional text, no markdown, no explanations outside the JSON structure."""

    def process_command(self, user_input: str) -> Dict[str, Any]:
        """
        Process user command and return structured JSON response from AI.
        Falls back to local processing if OpenAI is unavailable.
        
        Args:
            user_input: Natural language command from user
            
        Returns:
            Dict containing action, parameters, and reasoning
        """
        # Try local mode first if OpenAI unavailable or use_local_mode is enabled
        if self.use_local_mode or not self.openai_available:
            return self._process_local(user_input)
        
        try:
            # Add user message to history
            self.conversation_history.append({
                "role": "user",
                "content": user_input
            })
            
            # Prepare messages for API call
            messages = [
                {"role": "system", "content": self._get_system_prompt()},
                *self.conversation_history[-10:]  # Keep last 10 messages for context
            ]
            
            # Call OpenAI API
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                max_tokens=500
            )
            
            # Extract AI response
            ai_response = response.choices[0].message.content.strip()
            
            # Add assistant response to history
            self.conversation_history.append({
                "role": "assistant",
                "content": ai_response
            })
            
            # Parse JSON response
            command_dict = self._parse_ai_response(ai_response)
            
            return command_dict
            
        except Exception as e:
            error_str = str(e)
            
            # Check if it's a quota error
            if "429" in error_str or "quota" in error_str.lower():
                print(f"⚠️  OpenAI API quota exceeded. Switching to local mode...")
                self.use_local_mode = True
                return self._process_local(user_input)
            
            print(f"Error in AI processing: {e}")
            return {
                "action": "chat",
                "parameters": {
                    "response": f"I encountered an error processing your request: {str(e)}"
                },
                "reasoning": "Error occurred during processing"
            }
    
    def _parse_ai_response(self, response: str) -> Dict[str, Any]:
        """
        Parse and validate AI response JSON.
        
        Args:
            response: Raw response from OpenAI
            
        Returns:
            Validated command dictionary
        """
        try:
            # Remove markdown code blocks if present
            if response.startswith("```json"):
                response = response.replace("```json", "").replace("```", "").strip()
            elif response.startswith("```"):
                response = response.replace("```", "").strip()
            
            # Parse JSON
            command_dict = json.loads(response)
            
            # Validate required fields
            if "action" not in command_dict:
                raise ValueError("Response missing 'action' field")
            
            if "parameters" not in command_dict:
                command_dict["parameters"] = {}
            
            if "reasoning" not in command_dict:
                command_dict["reasoning"] = "No reasoning provided"
            
            return command_dict
            
        except json.JSONDecodeError as e:
            print(f"Failed to parse AI response as JSON: {response}")
            return {
                "action": "chat",
                "parameters": {
                    "response": "I had trouble formatting my response. Could you rephrase your request?"
                },
                "reasoning": "JSON parsing error"
            }
        except Exception as e:
            print(f"Error parsing AI response: {e}")
            return {
                "action": "chat",
                "parameters": {
                    "response": "I encountered an error. Please try again."
                },
                "reasoning": "Parsing error"
            }
    
    def clear_history(self) -> None:
        """Clear conversation history"""
        self.conversation_history = []
    
    def set_model(self, model: str) -> None:
        """Change the AI model being used"""
        self.model = model
    
    def _process_local(self, user_input: str) -> Dict[str, Any]:
        """
        Local command processing without OpenAI (fallback mode).
        Uses pattern matching to interpret common commands.
        
        Args:
            user_input: User's command
            
        Returns:
            Command dictionary
        """
        input_lower = user_input.lower().strip()
        
        # Application commands
        if re.search(r'\bopen\b', input_lower):
            app_match = re.search(r'open\s+([\w\s]+?)(?:\s|$)', input_lower)
            if app_match:
                app_name = app_match.group(1).strip()
                return {
                    "action": "open_app",
                    "parameters": {"app_name": app_name},
                    "reasoning": f"Opening {app_name} (local mode)"
                }
        
        if re.search(r'\bclose\b', input_lower):
            app_match = re.search(r'close\s+([\w\s]+?)(?:\s|$)', input_lower)
            if app_match:
                app_name = app_match.group(1).strip()
                return {
                    "action": "close_app",
                    "parameters": {"app_name": app_name},
                    "reasoning": f"Closing {app_name} (local mode)"
                }
        
        # Search commands
        if re.search(r'\bsearch\b', input_lower):
            query_match = re.search(r'search(?:\s+for)?\s+(.+)', input_lower)
            if query_match:
                query = query_match.group(1).strip()
                engine = "google"
                if "youtube" in input_lower:
                    engine = "youtube"
                elif "bing" in input_lower:
                    engine = "bing"
                return {
                    "action": "search_web",
                    "parameters": {"query": query, "engine": engine},
                    "reasoning": f"Searching for '{query}' (local mode)"
                }
        
        # URL opening
        if re.search(r'\b(go to|open|visit)\b.*\.(com|org|net|io|co)', input_lower):
            url_match = re.search(r'([\w-]+\.(?:com|org|net|io|co|uk|gov)(?:/[\w-]*)?)', input_lower)
            if url_match:
                url = url_match.group(1)
                return {
                    "action": "open_url",
                    "parameters": {"url": url},
                    "reasoning": f"Opening {url} (local mode)"
                }
        
        # Web automation commands
        if "read" in input_lower and ("page" in input_lower or "webpage" in input_lower or "website" in input_lower):
            return {
                "action": "read_webpage",
                "parameters": {},
                "reasoning": "Reading current webpage content (local mode)"
            }
        
        if "page info" in input_lower or "webpage info" in input_lower:
            return {
                "action": "get_webpage_info",
                "parameters": {},
                "reasoning": "Getting webpage information (local mode)"
            }
        
        if "screenshot" in input_lower and ("page" in input_lower or "webpage" in input_lower):
            return {
                "action": "webpage_screenshot",
                "parameters": {},
                "reasoning": "Taking webpage screenshot (local mode)"
            }
        
        if "close browser" in input_lower or "close chrome" in input_lower:
            return {
                "action": "close_browser",
                "parameters": {},
                "reasoning": "Closing browser (local mode)"
            }
        
        if "browse to" in input_lower or "navigate to" in input_lower:
            url_match = re.search(r'(?:browse|navigate)\s+to\s+(.+)', input_lower)
            if url_match:
                url = url_match.group(1).strip()
                return {
                    "action": "browse_to",
                    "parameters": {"url": url},
                    "reasoning": f"Navigating to {url} (local mode)"
                }
        
        if "search and open" in input_lower or "search and browse" in input_lower:
            query_match = re.search(r'search\s+and\s+(?:open|browse)\s+(.+)', input_lower)
            if query_match:
                query = query_match.group(1).strip()
                return {
                    "action": "search_and_browse",
                    "parameters": {"query": query},
                    "reasoning": f"Searching and opening first result for '{query}' (local mode)"
                }
        
        if "start browser" in input_lower or ("open" in input_lower and "browser" in input_lower):
            return {
                "action": "start_browser",
                "parameters": {},
                "reasoning": "Starting browser (local mode)"
            }
        
        # File operations
        if "create file" in input_lower or "make file" in input_lower:
            file_match = re.search(r'(?:create|make)\s+(?:a\s+)?file\s+(?:called\s+)?([\w.-]+)', input_lower)
            if file_match:
                filename = file_match.group(1)
                return {
                    "action": "create_file",
                    "parameters": {"file_path": filename, "content": ""},
                    "reasoning": f"Creating file {filename} (local mode)"
                }
        
        if "create folder" in input_lower or "make folder" in input_lower:
            folder_match = re.search(r'(?:create|make)\s+(?:a\s+)?folder\s+(?:called\s+)?([\w.-]+)', input_lower)
            if folder_match:
                foldername = folder_match.group(1)
                return {
                    "action": "create_folder",
                    "parameters": {"folder_path": foldername},
                    "reasoning": f"Creating folder {foldername} (local mode)"
                }
        
        if "list files" in input_lower or "show files" in input_lower:
            dir_match = re.search(r'(?:list|show)\s+files\s+(?:in\s+)?([\w./\\-]+)', input_lower)
            directory = dir_match.group(1) if dir_match else "."
            return {
                "action": "list_files",
                "parameters": {"directory_path": directory},
                "reasoning": "Listing files (local mode)"
            }
        
        if "organize downloads" in input_lower or "clean downloads" in input_lower:
            return {
                "action": "organize_downloads",
                "parameters": {},
                "reasoning": "Organizing downloads folder (local mode)"
            }
        
        # System commands
        if "system info" in input_lower or "system information" in input_lower:
            return {
                "action": "chat",
                "parameters": {"response": "System info command detected but not yet implemented in local mode. This requires the system.get_system_info() function."},
                "reasoning": "System info request (local mode)"
            }
        
        if "time" in input_lower or "date" in input_lower:
            from datetime import datetime
            now = datetime.now()
            date_str = now.strftime("%A, %B %d, %Y")
            time_str = now.strftime("%I:%M:%S %p")
            return {
                "action": "chat",
                "parameters": {"response": f"📅 {date_str}\n🕐 {time_str}"},
                "reasoning": "Time/date request (local mode)"
            }
        
        if "news" in input_lower:
            return {
                "action": "get_news",
                "parameters": {"category": "general"},
                "reasoning": "Fetching news (local mode)"
            }
        
        if "screenshot" in input_lower or "take screenshot" in input_lower:
            return {
                "action": "take_screenshot",
                "parameters": {},
                "reasoning": "Taking screenshot (local mode)"
            }
        
        # Mouse/keyboard
        if "click" in input_lower:
            coord_match = re.search(r'click\s+(?:at\s+)?(?:\()?\s*(\d+)\s*,\s*(\d+)', input_lower)
            if coord_match:
                x, y = int(coord_match.group(1)), int(coord_match.group(2))
                return {
                    "action": "mouse_click",
                    "parameters": {"x": x, "y": y, "button": "left"},
                    "reasoning": f"Clicking at ({x}, {y}) (local mode)"
                }
        
        if "type" in input_lower:
            type_match = re.search(r'type\s+(.+)', input_lower)
            if type_match:
                text = type_match.group(1).strip()
                return {
                    "action": "type_text",
                    "parameters": {"text": text},
                    "reasoning": "Typing text (local mode)"
                }
        
        # Default: chat response
        return {
            "action": "chat",
            "parameters": {
                "response": f"I'm running in local mode (OpenAI unavailable). I understood: '{user_input}' but couldn't match it to a command. Try: 'open chrome', 'search for python', 'create folder test', 'list files', 'get news', or 'help'."
            },
            "reasoning": "Unrecognized command (local mode)"
        }


# Global AI brain instance
ai_brain = AIBrain()
