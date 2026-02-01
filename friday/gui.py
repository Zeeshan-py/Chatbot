"""
FRIDAY GUI - Modern Professional Interface
Beautiful dark theme with smooth animations
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
from datetime import datetime
from pathlib import Path
import sys

# Add friday to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from friday.ai_brain import ai_brain
from friday.command_parser import command_parser


class FridayGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("FRIDAY - AI Desktop Assistant")
        self.root.geometry("1000x700")
        self.root.minsize(800, 600)
        
        # Modern dark theme colors
        self.colors = {
            'bg_dark': '#1a1a2e',
            'bg_medium': '#16213e',
            'bg_light': '#0f3460',
            'accent': '#00d4ff',
            'accent_hover': '#00b8e6',
            'text': '#e8e8e8',
            'text_dim': '#a0a0a0',
            'success': '#00ff88',
            'warning': '#ffa500',
            'error': '#ff4444',
            'user_msg': '#2d4059',
            'ai_msg': '#0f3460',
        }
        
        self.root.configure(bg=self.colors['bg_dark'])
        
        # Initialize components
        self.ai = ai_brain
        self.parser = command_parser
        self.processing = False
        
        self.setup_ui()
        self.add_welcome_message()
        
    def setup_ui(self):
        """Create the main UI layout"""
        
        # ===== TOP BAR =====
        top_bar = tk.Frame(self.root, bg=self.colors['bg_medium'], height=60)
        top_bar.pack(fill='x', side='top')
        top_bar.pack_propagate(False)
        
        # Logo/Title
        title_frame = tk.Frame(top_bar, bg=self.colors['bg_medium'])
        title_frame.pack(side='left', padx=20, pady=10)
        
        title_label = tk.Label(
            title_frame,
            text="F R I D A Y",
            font=('Segoe UI', 24, 'bold'),
            fg=self.colors['accent'],
            bg=self.colors['bg_medium']
        )
        title_label.pack(side='left')
        
        subtitle_label = tk.Label(
            title_frame,
            text="AI Desktop Assistant",
            font=('Segoe UI', 10),
            fg=self.colors['text_dim'],
            bg=self.colors['bg_medium']
        )
        subtitle_label.pack(side='left', padx=10)
        
        # Status indicator
        self.status_frame = tk.Frame(top_bar, bg=self.colors['bg_medium'])
        self.status_frame.pack(side='right', padx=20)
        
        self.status_dot = tk.Label(
            self.status_frame,
            text="●",
            font=('Arial', 20),
            fg=self.colors['success'],
            bg=self.colors['bg_medium']
        )
        self.status_dot.pack(side='left')
        
        self.status_label = tk.Label(
            self.status_frame,
            text="Ready",
            font=('Segoe UI', 11),
            fg=self.colors['text'],
            bg=self.colors['bg_medium']
        )
        self.status_label.pack(side='left', padx=5)
        
        # ===== MAIN CONTENT AREA =====
        content_frame = tk.Frame(self.root, bg=self.colors['bg_dark'])
        content_frame.pack(fill='both', expand=True, padx=2, pady=2)
        
        # Left sidebar
        self.create_sidebar(content_frame)
        
        # Chat area
        self.create_chat_area(content_frame)
        
        # ===== BOTTOM INPUT AREA =====
        self.create_input_area()
        
    def create_sidebar(self, parent):
        """Create left sidebar with controls"""
        sidebar = tk.Frame(parent, bg=self.colors['bg_medium'], width=250)
        sidebar.pack(side='left', fill='y', padx=(0, 2))
        sidebar.pack_propagate(False)
        
        # Mode section
        mode_frame = tk.LabelFrame(
            sidebar,
            text="  Mode  ",
            font=('Segoe UI', 11, 'bold'),
            fg=self.colors['accent'],
            bg=self.colors['bg_medium'],
            relief='flat'
        )
        mode_frame.pack(fill='x', padx=15, pady=20)
        
        # AI Mode indicator
        self.ai_mode_label = tk.Label(
            mode_frame,
            text="● Local Mode",
            font=('Segoe UI', 10),
            fg=self.colors['text'],
            bg=self.colors['bg_medium'],
            anchor='w'
        )
        self.ai_mode_label.pack(fill='x', padx=10, pady=5)
        
        # Safety level
        self.safety_label = tk.Label(
            mode_frame,
            text="🛡️ Safe Mode",
            font=('Segoe UI', 10),
            fg=self.colors['success'],
            bg=self.colors['bg_medium'],
            anchor='w'
        )
        self.safety_label.pack(fill='x', padx=10, pady=5)
        
        # Advanced mode toggle
        adv_frame = tk.Frame(mode_frame, bg=self.colors['bg_medium'])
        adv_frame.pack(fill='x', padx=10, pady=10)
        
        self.advanced_var = tk.BooleanVar()
        advanced_check = tk.Checkbutton(
            adv_frame,
            text="Advanced Mode",
            variable=self.advanced_var,
            command=self.toggle_advanced_mode,
            font=('Segoe UI', 10),
            fg=self.colors['text'],
            bg=self.colors['bg_medium'],
            selectcolor=self.colors['bg_light'],
            activebackground=self.colors['bg_medium'],
            activeforeground=self.colors['accent']
        )
        advanced_check.pack(anchor='w')
        
        # Quick actions
        actions_frame = tk.LabelFrame(
            sidebar,
            text="  Quick Actions  ",
            font=('Segoe UI', 11, 'bold'),
            fg=self.colors['accent'],
            bg=self.colors['bg_medium'],
            relief='flat'
        )
        actions_frame.pack(fill='x', padx=15, pady=10)
        
        quick_actions = [
            ("🌐 Open Chrome", "open chrome"),
            ("📸 Screenshot", "take screenshot"),
            ("🕐 Time & Date", "what time is it"),
            ("📰 Get News", "get news"),
            ("🔍 Search Web", None),
        ]
        
        for label, command in quick_actions:
            btn = tk.Button(
                actions_frame,
                text=label,
                command=lambda c=command: self.quick_action(c),
                font=('Segoe UI', 9),
                fg=self.colors['text'],
                bg=self.colors['bg_light'],
                activebackground=self.colors['accent'],
                activeforeground='white',
                relief='flat',
                cursor='hand2',
                pady=8
            )
            btn.pack(fill='x', padx=10, pady=3)
            btn.bind('<Enter>', lambda e, b=btn: b.config(bg=self.colors['accent']))
            btn.bind('<Leave>', lambda e, b=btn: b.config(bg=self.colors['bg_light']))
        
        # Clear chat button
        clear_btn = tk.Button(
            sidebar,
            text="🗑️ Clear Chat",
            command=self.clear_chat,
            font=('Segoe UI', 10, 'bold'),
            fg=self.colors['text'],
            bg=self.colors['error'],
            activebackground='#cc0000',
            activeforeground='white',
            relief='flat',
            cursor='hand2',
            pady=10
        )
        clear_btn.pack(fill='x', padx=15, pady=20, side='bottom')
        
    def create_chat_area(self, parent):
        """Create main chat display area"""
        chat_container = tk.Frame(parent, bg=self.colors['bg_dark'])
        chat_container.pack(side='left', fill='both', expand=True)
        
        # Chat display
        self.chat_display = scrolledtext.ScrolledText(
            chat_container,
            font=('Segoe UI', 11),
            bg=self.colors['bg_dark'],
            fg=self.colors['text'],
            insertbackground=self.colors['accent'],
            relief='flat',
            wrap='word',
            padx=20,
            pady=20,
            spacing3=10
        )
        self.chat_display.pack(fill='both', expand=True)
        
        # Configure tags for message styling
        self.chat_display.tag_config('user', 
            foreground=self.colors['text'],
            background=self.colors['user_msg'],
            spacing1=5,
            spacing3=5,
            lmargin1=10,
            lmargin2=10,
            rmargin=10
        )
        
        self.chat_display.tag_config('ai',
            foreground=self.colors['text'],
            background=self.colors['ai_msg'],
            spacing1=5,
            spacing3=5,
            lmargin1=10,
            lmargin2=10,
            rmargin=10
        )
        
        self.chat_display.tag_config('success',
            foreground=self.colors['success'],
            font=('Segoe UI', 10, 'bold')
        )
        
        self.chat_display.tag_config('error',
            foreground=self.colors['error'],
            font=('Segoe UI', 10, 'bold')
        )
        
        self.chat_display.tag_config('info',
            foreground=self.colors['accent'],
            font=('Segoe UI', 10)
        )
        
        self.chat_display.tag_config('time',
            foreground=self.colors['text_dim'],
            font=('Segoe UI', 9)
        )
        
    def create_input_area(self):
        """Create bottom input area"""
        input_container = tk.Frame(self.root, bg=self.colors['bg_medium'], height=100)
        input_container.pack(fill='x', side='bottom')
        input_container.pack_propagate(False)
        
        # Input frame
        input_frame = tk.Frame(input_container, bg=self.colors['bg_medium'])
        input_frame.pack(fill='both', expand=True, padx=20, pady=15)
        
        # Text input
        self.input_field = tk.Text(
            input_frame,
            font=('Segoe UI', 12),
            bg=self.colors['bg_light'],
            fg=self.colors['text'],
            insertbackground=self.colors['accent'],
            relief='flat',
            height=2,
            wrap='word',
            padx=15,
            pady=10
        )
        self.input_field.pack(side='left', fill='both', expand=True)
        self.input_field.bind('<Return>', self.on_enter)
        self.input_field.bind('<Shift-Return>', lambda e: None)
        self.input_field.focus()
        
        # Send button
        self.send_btn = tk.Button(
            input_frame,
            text="SEND",
            command=self.send_message,
            font=('Segoe UI', 11, 'bold'),
            fg='white',
            bg=self.colors['accent'],
            activebackground=self.colors['accent_hover'],
            activeforeground='white',
            relief='flat',
            cursor='hand2',
            width=10,
            padx=20
        )
        self.send_btn.pack(side='right', fill='y', padx=(10, 0))
        
    def add_welcome_message(self):
        """Display welcome message"""
        welcome = """
╔══════════════════════════════════════════════════════════════╗
║                    Welcome to FRIDAY                          ║
║              AI-Powered Desktop Assistant                     ║
╚══════════════════════════════════════════════════════════════╝

✨ I'm ready to help you automate your computer!

Quick start:
• Type your command naturally (e.g., "open chrome")
• Enable Advanced Mode for system-level control
• Use Quick Actions on the left for common tasks

Type 'help' to see all available commands.
"""
        self.add_message(welcome, 'ai')
        
    def add_message(self, text, msg_type='ai', tag=None):
        """Add message to chat with styling"""
        self.chat_display.config(state='normal')
        
        # Add timestamp
        timestamp = datetime.now().strftime("%H:%M")
        
        if msg_type == 'user':
            self.chat_display.insert('end', f"\n👤 You ({timestamp})\n", 'time')
            self.chat_display.insert('end', f"{text}\n", 'user')
        else:
            self.chat_display.insert('end', f"\n🤖 FRIDAY ({timestamp})\n", 'time')
            if tag:
                self.chat_display.insert('end', f"{text}\n", tag)
            else:
                self.chat_display.insert('end', f"{text}\n", 'ai')
        
        self.chat_display.config(state='disabled')
        self.chat_display.see('end')
        
    def send_message(self):
        """Process and send user message"""
        user_input = self.input_field.get('1.0', 'end-1c').strip()
        
        if not user_input or self.processing:
            return
        
        # Clear input
        self.input_field.delete('1.0', 'end')
        
        # Add user message
        self.add_message(user_input, 'user')
        
        # Process in background thread
        self.processing = True
        self.update_status("Processing...", self.colors['warning'])
        threading.Thread(target=self.process_command, args=(user_input,), daemon=True).start()
        
    def process_command(self, user_input):
        """Process command in background"""
        try:
            # Handle special commands
            if user_input.lower() in ['exit', 'quit']:
                self.root.after(0, self.root.quit)
                return
            
            if user_input.lower() == 'help':
                help_text = """
🔹 Application Control: open chrome, close notepad
🔹 Web Browsing: search for python, open youtube.com
🔹 File Management: create file test.txt, list files
🔹 System: what time is it, get news, take screenshot
🔹 Advanced: execute command dir, read file config.txt
🔹 Special: help, clear, status, advanced mode on/off
"""
                self.root.after(0, lambda: self.add_message(help_text, 'ai', 'info'))
                self.root.after(0, lambda: self.update_status("Ready", self.colors['success']))
                self.processing = False
                return
            
            if user_input.lower() == 'clear':
                self.root.after(0, self.clear_chat)
                self.processing = False
                return
            
            # Process with AI
            command = self.ai.process_command(user_input)
            result = self.parser.parse_and_execute(command, auto_confirm=False)
            
            # Display result
            if result.get('success'):
                self.root.after(0, lambda: self.add_message(result['message'], 'ai', 'success'))
            else:
                self.root.after(0, lambda: self.add_message(result['message'], 'ai', 'error'))
            
        except Exception as e:
            error_msg = f"❌ Error: {str(e)}"
            self.root.after(0, lambda: self.add_message(error_msg, 'ai', 'error'))
        
        finally:
            self.root.after(0, lambda: self.update_status("Ready", self.colors['success']))
            self.processing = False
    
    def on_enter(self, event):
        """Handle Enter key"""
        if not event.state & 0x1:  # Not Shift+Enter
            self.send_message()
            return 'break'
    
    def toggle_advanced_mode(self):
        """Toggle advanced mode"""
        self.parser.advanced_mode = self.advanced_var.get()
        if self.parser.advanced_mode:
            self.safety_label.config(
                text="⚠️  Advanced Mode",
                fg=self.colors['warning']
            )
            self.add_message("⚠️ Advanced Mode Enabled - Broader system control active", 'ai', 'info')
        else:
            self.safety_label.config(
                text="🛡️ Safe Mode",
                fg=self.colors['success']
            )
            self.add_message("✅ Advanced Mode Disabled - Back to safe mode", 'ai', 'info')
    
    def quick_action(self, command):
        """Execute quick action"""
        if command:
            self.input_field.delete('1.0', 'end')
            self.input_field.insert('1.0', command)
            self.send_message()
        else:
            # Search prompt
            self.input_field.delete('1.0', 'end')
            self.input_field.insert('1.0', 'search for ')
            self.input_field.focus()
    
    def clear_chat(self):
        """Clear chat history"""
        self.chat_display.config(state='normal')
        self.chat_display.delete('1.0', 'end')
        self.chat_display.config(state='disabled')
        self.add_welcome_message()
    
    def update_status(self, text, color):
        """Update status indicator"""
        self.status_label.config(text=text)
        self.status_dot.config(fg=color)
    
    def run(self):
        """Start the GUI"""
        self.root.mainloop()


def main():
    """Launch FRIDAY GUI"""
    app = FridayGUI()
    app.run()


if __name__ == "__main__":
    main()
