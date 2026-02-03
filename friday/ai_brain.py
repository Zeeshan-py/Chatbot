"""
FRIDAY AI Brain Module
Handles communication with OpenAI API using the "Tools" (Function Calling) architecture.
This enables the Agentic Loop: Think -> Act -> Observe -> Think.
Includes ROBUST LOCAL FALLBACK for offline/quota-exceeded scenarios.
"""

import json
import traceback
import re
from typing import Dict, Any, List, Optional
from openai import OpenAI, RateLimitError, APIError, APIConnectionError
from friday.config import config
from friday.actions import apps, files, browser, system, advanced, web_automation

class AIBrain:
    """
    Agentic Brain that uses OpenAI's Tools API to perform multi-step tasks.
    Falls back to Regex-based Local Mode if API is unavailable.
    """
    
    def __init__(self):
        try:
            self.client = OpenAI(api_key=config.openai_api_key)
            self.model = "gpt-4-turbo" 
            self.openai_available = True
        except Exception:
            self.client = None
            self.openai_available = False
        
        self.conversation_history = []
        self.use_local_mode = not self.openai_available
        self.max_steps = 15  # Prevent infinite loops
        
        # Define available tools for the AI
        self.tools = self._get_tools_schema()
        
        # Map tool names to actual functions
        self.available_functions = {
            "run_terminal_command": advanced.execute_system_command,
            "open_app": apps.open_application,
            "close_app": apps.close_application,
            "google_search": web_automation.google_search,
            "read_webpage": web_automation.read_webpage,
            "browse_to": web_automation.navigate_to,
            "web_click": web_automation.click_element,
            "web_type": web_automation.fill_form,
            "create_file": files.create_file,
            "read_file": advanced.read_any_file,
            "list_files": files.list_files,
            "get_current_time": system.get_time,
        }

    def _get_system_prompt(self) -> str:
        return """You are FRIDAY, an advanced autonomous AI agent running on a Windows laptop.

CAPABILITIES:
1. **OS Access**: You can run ANY terminal command using `run_terminal_command`. Use PowerShell syntax.
2. **Web Research**: You can search Google and browse websites to find information.
3. **Planning**: You can break down complex tasks into steps.
4. **File Management**: You can create, read, and edit files.

PERFORMANCE TIPS:
- **Think First**: Before taking action, analyze the user's request.
- **Be Resourceful**: If one method fails, try another.
- **Verify**: Check if your actions succeeded.
- **Privacy**: Do not upload personal user data.

CURRENT CONTEXT:
- OS: Windows
- User: Boss / Sir
- Current Directory: Project Root
"""

    def _get_tools_schema(self) -> List[Dict[str, Any]]:
        """Define the tools available to the AI"""
        return [
            {
                "type": "function",
                "function": {
                    "name": "run_terminal_command",
                    "description": "Execute a PowerShell command on the local machine.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "command": {"type": "string", "description": "The PowerShell command to run"}
                        },
                        "required": ["command"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "google_search",
                    "description": "Search Google for information.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "query": {"type": "string", "description": "Search query"},
                            "open_first": {"type": "boolean", "description": "Open first result (default: False)"}
                        },
                        "required": ["query"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "open_app",
                    "description": "Launch a desktop application.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "app_name": {"type": "string", "description": "Name of the application"}
                        },
                        "required": ["app_name"]
                    }
                }
            },
             {
                "type": "function",
                "function": {
                    "name": "browse_to",
                    "description": "Navigate the browser to a URL.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "url": {"type": "string", "description": "The URL to visit"}
                        },
                        "required": ["url"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "read_webpage",
                    "description": "Read text from current webpage.",
                    "parameters": {"type": "object", "properties": {}}
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "create_file",
                    "description": "Create a new file.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "file_path": {"type": "string", "description": "Path to new file"},
                            "content": {"type": "string", "description": "File content"}
                        },
                        "required": ["file_path", "content"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "read_file",
                    "description": "Read a local file.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "file_path": {"type": "string", "description": "Path to the file"}
                        },
                        "required": ["file_path"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "list_files",
                    "description": "List files in a directory.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "directory_path": {"type": "string", "description": "Directory to list"}
                        },
                        "required": ["directory_path"]
                    }
                }
            }
        ]

    def process_command(self, user_input: str) -> Dict[str, Any]:
        """
        Main Agentic Loop with Error Handling and Local Fallback.
        """
        # Global local mode switch
        if self.use_local_mode or not self.openai_available:
            return self._process_local(user_input)

        self.conversation_history.append({"role": "user", "content": user_input})
        step_count = 0
        
        while step_count < self.max_steps:
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": self._get_system_prompt()},
                        *self.conversation_history
                    ],
                    tools=self.tools,
                    tool_choice="auto",
                    temperature=0.0
                )
                
                response_message = response.choices[0].message
                
                if response_message.tool_calls:
                    self.conversation_history.append(response_message)
                    
                    for tool_call in response_message.tool_calls:
                        function_name = tool_call.function.name
                        function_args = json.loads(tool_call.function.arguments)
                        
                        print(f"🔧 Agent is calling tool: {function_name} with args: {function_args}")
                        
                        function_to_call = self.available_functions.get(function_name)
                        
                        if function_to_call:
                            try:
                                if function_name == "run_terminal_command":
                                    function_response = function_to_call(function_args.get("command"))
                                elif function_name == "google_search":
                                     function_response = function_to_call(function_args.get("query"), function_args.get("open_first", False))
                                elif function_name == "create_file":
                                     function_response = function_to_call(function_args.get("file_path"), function_args.get("content"))
                                elif function_name == "read_file":
                                     function_response = function_to_call(function_args.get("file_path"))
                                elif function_name == "open_app":
                                     function_response = function_to_call(function_args.get("app_name"))
                                elif function_name == "browse_to":
                                     function_response = function_to_call(function_args.get("url"))
                                else:
                                     function_response = function_to_call(**function_args)
                            except Exception as e:
                                function_response = f"Error executing tool {function_name}: {str(e)}\n{traceback.format_exc()}"
                        else:
                            function_response = f"Error: Tool {function_name} not found."

                        self.conversation_history.append({
                            "role": "tool",
                            "tool_call_id": tool_call.id,
                            "name": function_name,
                            "content": str(function_response)
                        })
                    step_count += 1
                else:
                    final_response = response_message.content
                    self.conversation_history.append({"role": "assistant", "content": final_response})
                    return {
                        "action": "chat",
                        "parameters": {"response": final_response},
                        "reasoning": "Task completed."
                    }
                    
            except (RateLimitError, APIConnectionError) as e:
                print(f"\n⚠️  OpenAI API Error: {str(e)}")
                print("🔄 Automatic Fallback: Switching to LOCAL MODE...")
                self.use_local_mode = True
                self.openai_available = False
                return self._process_local(user_input)
                
            except Exception as e:
                print(f"CRITICAL ERROR in Agent Loop: {e}")
                return {
                    "action": "chat",
                    "parameters": {"response": f"I encountered a critical error: {e}"},
                    "reasoning": "Crash"
                }
        
        return {
            "action": "chat",
            "parameters": {"response": "I reached my maximum step limit."},
            "reasoning": "Max steps reached"
        }

    def _process_local(self, user_input: str) -> Dict[str, Any]:
        """
        Legacy local mode fallback using Regex Pattern Matching.
        Allows basic usage without OpenAI.
        """
        input_lower = user_input.lower().strip()
        
        # 1. App Opening
        if re.search(r'\bopen\b', input_lower):
            app_match = re.search(r'open\s+([\w\s]+?)(?:\s|$)', input_lower)
            if app_match:
                app_name = app_match.group(1).strip()
                return {
                    "action": "open_app",
                    "parameters": {"app_name": app_name},
                    "reasoning": f"Opening {app_name} (local mode)"
                }
        
        # 2. Web Search (Compound or Direct)
        # Handle "open chrome and search ..." or just "search ..."
        if re.search(r'\bsearch\b', input_lower):
            query_match = re.search(r'search(?:\s+for)?\s+(.+)', input_lower)
            if query_match:
                query = query_match.group(1).strip()
                # If "and" is present, split and take the last part as query if it makes sense
                if " and " in query:
                    parts = query.split(" and ")
                    query = parts[-1] # simplistic assumption
                
                return {
                    "action": "google_search",
                    "parameters": {"query": query, "open_first": True},
                    "reasoning": f"Searching for '{query}' (local mode)"
                }

        # 3. App Closign
        if re.search(r'\bclose\b', input_lower):
            app_match = re.search(r'close\s+([\w\s]+?)(?:\s|$)', input_lower)
            if app_match:
                app_name = app_match.group(1).strip()
                return {
                    "action": "close_app",
                    "parameters": {"app_name": app_name},
                    "reasoning": f"Closing {app_name} (local mode)"
                }

        # 4. System Info
        if "time" in input_lower or "date" in input_lower:
            return {
                "action": "chat",
                "parameters": {"response": system.get_time()},
                "reasoning": "Time request (local mode)"
            }

        # 5. List Files
        if "list files" in input_lower:
             return {
                "action": "list_files",
                "parameters": {"directory_path": "."},
                "reasoning": "Listing files (local mode)"
            }

        return {
            "action": "chat",
            "parameters": {"response": "I am in LOCAL MODE (Offline). I can understand basic commands like 'open chrome', 'search for X', 'what time is it'. For complex tasks, I need a working OpenAI key."},
            "reasoning": "Offline mode"
        }

# Global AI brain instance
ai_brain = AIBrain()
