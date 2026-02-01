# 🤖 FRIDAY - AI-Powered Desktop Automation Assistant

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--3.5-orange.svg)](https://openai.com/)

A secure, production-ready AI desktop assistant that uses OpenAI to interpret natural language commands and execute safe, whitelisted automation functions. Works with or without OpenAI (local fallback mode).

## 📋 Table of Contents
- [Features](#-features)
- [Quick Start](#-quick-start)
- [Installation](#-detailed-installation)
- [Usage](#-usage-guide)
- [Commands](#-available-commands)
- [Security](#-security-features)
- [Configuration](#-configuration)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)
- [License](#-license)

## ✨ Features

- 🔐 **Security-First Architecture** - Command whitelist prevents arbitrary code execution
- 🧠 **Dual-Mode Operation** - AI mode (OpenAI) + Local mode (pattern matching)
- 🎯 **Auto-Fallback** - Automatically switches to local mode if OpenAI quota exceeded
- 🌐 **Web Automation (NEW!)** - Full Selenium browser control with default profile, search, read pages, screenshots
- 🖥️ **Application Control** - Open/close any application (Chrome, Firefox, Edge, WhatsApp, Discord, Spotify)
- 🔍 **Web Search** - Google, Bing, YouTube, DuckDuckGo integration
- 📁 **File Management** - Create, delete, move, organize files
- 🖱️ **Mouse & Keyboard** - Full input automation
- 📸 **Screenshots** - Capture screen content or specific webpages
- 📰 **News Integration** - Fetch latest headlines
- 💻 **System Information** - CPU, RAM, disk, battery status
- 🎨 **Modern GUI** - Beautiful dark-themed interface with quick actions
- 🚀 **Advanced Mode** - System commands, Python execution, PowerShell (toggle on/off)
- 🤖 **Claude-Level Powers** - Computer use agent capabilities for web browsing

> **NEW: Web Automation Super Powers!** See [WEB_AUTOMATION_GUIDE.md](WEB_AUTOMATION_GUIDE.md) for full details.

## 🚀 Quick Start

**Just want to get started?** Here's the fastest way:

```bash
# 1. Clone and navigate
git clone <your-repo-url>
cd "Mega project"

# 2. Setup virtual environment
python -m venv .venv
.venv\Scripts\activate          # Windows
# source .venv/bin/activate     # macOS/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create .env file (copy template)
copy .env.example .env          # Windows
# cp .env.example .env          # macOS/Linux

# 5. Run FRIDAY
python -m friday.main
```

**That's it!** FRIDAY works in local mode without API keys. Add OpenAI key later for AI mode.

---

## 🔧 Detailed Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)
- Git (for version control)

### Step-by-Step Setup

#### 1. Clone the Repository
```bash
git clone <your-repository-url>
cd "Mega project"
```

#### 2. Create Virtual Environment
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# macOS/Linux
python3 -m venv .venv
source .venv/bin/activate
```

#### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

#### 4. Configure Environment Variables

Copy the template:
```bash
# Windows
copy .env.example .env

# macOS/Linux
cp .env.example .env
```

Edit `.env` file:
```env
# Required for AI mode (optional for local mode)
OPENAI_API_KEY=sk-your-actual-openai-api-key-here

# Optional - for news features
NEWS_API_KEY=your-news-api-key-here
```

**Get API Keys:**
- OpenAI: https://platform.openai.com/api-keys
- News API: https://newsapi.org (Optional, 100 free requests/day)

#### 5. Run FRIDAY
```bash
python -m friday.main
```

---

## 📖 Usage Guide

### ⚠️ IMPORTANT: Command Format

**Type commands WITHOUT quotes!**

✅ **CORRECT:**
```
You: open chrome
You: search for python tutorials
You: what time is it
```

❌ **WRONG:**
```
You: "open chrome"        ❌ Don't use quotes
You: 'search for python'  ❌ Don't use quotes
```

### Basic Usage Examples

```
👤 You: open chrome
✅ Opening chrome...

👤 You: search for python tutorials
✅ Searching for 'python tutorials' on Google

👤 You: create folder Projects
✅ Created folder: C:\Users\You\Projects

👤 You: what time is it?
🤖 FRIDAY: 📅 Sunday, February 01, 2026
           🕐 02:30:45 PM

👤 You: get news
📰 Top General News:
1. Article headline...
2. Another headline...
```

### Special Commands
```
help      - Show all available commands
clear     - Clear conversation history
mode      - Check current mode (AI/Local)
exit      - Exit FRIDAY
```

---

## 📝 Available Commands

### 🖥️ Application Control
Auto-detects popular applications:
```
open chrome          # Google Chrome
open firefox         # Mozilla Firefox
open edge            # Microsoft Edge
open notepad         # Notepad
open code            # VS Code
close chrome         # Close Chrome
```

### 🌐 Web Browsing
```
search for python tutorials
open youtube.com
go to github.com
```

### 📁 File Management
```
create file test.txt
create folder MyProject
list files
list files in Downloads
delete file test.txt
move file.txt to Documents
copy file.txt to Desktop
organize downloads
```

### 🖱️ Mouse & Keyboard
```
click at 500, 300
move mouse to 800, 600
type Hello World
press enter
take screenshot
```

### 💻 System Information
```
what time is it
get system info
battery status
get news
```

### ⚙️ Special Commands
```
help         - Show this help
clear        - Clear conversation history
mode         - Check AI/Local mode status
exit/quit    - Exit FRIDAY
```

## 🔐 Security Features

### Command Whitelist
✅ Only pre-approved functions can execute  
❌ AI cannot run arbitrary commands  
❌ No shell injection possible  

### Protected Paths
System directories are blocked:
- Windows: `C:\Windows`, `C:\Program Files`
- Linux/Mac: `/System`, `/usr/bin`, `/bin`

### User Confirmation
Risky operations require explicit approval:
- File deletion
- Folder organization
- Application closing
- Bulk file operations

---

## 📁 Project Structure

```
Mega project/
├── friday/                 # Main FRIDAY framework
│   ├── main.py            # Entry point
│   ├── ai_brain.py        # AI + Local processing
│   ├── command_parser.py  # Command validation & routing
│   ├── config.py          # Environment configuration
│   ├── utils.py           # Helper functions & UI
│   └── actions/           # Automation modules
│       ├── apps.py        # Application control
│       ├── files.py       # File operations
│       ├── browser.py     # Web automation
│       ├── system.py      # System information
│       └── mouse_keyboard.py  # Input automation
├── check_safety.py        # Pre-commit security check
├── .env                   # Your API keys (DO NOT COMMIT!)
├── .env.example           # Environment template
├── .gitignore            # Git ignore rules
├── requirements.txt       # Python dependencies
├── README.md             # This file
└── GITHUB_CHECKLIST.md   # Pre-commit checklist
```

---

## ⚙️ Configuration

### Environment Variables

Create `.env` file from template:
```env
# Required for AI mode (optional for local mode)
OPENAI_API_KEY=sk-your-key-here

# Optional - for news features
NEWS_API_KEY=your-key-here
```

### Mode Selection

FRIDAY operates in two modes:

**1. AI Mode (OpenAI)**
- Uses GPT-3.5-Turbo for natural language understanding
- Better command interpretation
- Requires API key and credits
- Cost: ~$0.001-0.003 per command

**2. Local Mode (Pattern Matching)**
- Works completely offline
- Free forever
- Uses regex pattern matching
- Automatic fallback if OpenAI quota exceeded

### Security Settings

Edit `friday/config.py` to customize:
```python
SAFETY_SETTINGS = {
    "require_confirmation_for": [
        "delete_file",
        "delete_folder",
        "organize_downloads",
        "close_app"
    ],
    "blocked_paths": [
        "C:\\Windows",
        "C:\\Program Files",
        "/System",
        "/usr/bin"
    ]
}
```

---

## 🐛 Troubleshooting

### Common Issues

#### 1. OpenAI Quota Exceeded
```
⚠️ OpenAI API quota exceeded. Switching to local mode...
```
**Solutions:**
- ✅ Continue using local mode (free)
- 💳 Add credits: https://platform.openai.com/account/billing
- 📝 New accounts get $5 free credit

#### 2. Module Not Found Error
```
ModuleNotFoundError: No module named 'openai'
```
**Solution:**
```bash
pip install -r requirements.txt
```

#### 3. API Key Not Found
```
ERROR: OPENAI_API_KEY not found in .env file
```
**Solutions:**
- Check `.env` file exists in project root
- Verify `OPENAI_API_KEY=sk-...` is set correctly
- No extra spaces or quotes around the key
- Restart FRIDAY after editing `.env`

#### 4. Chrome/Application Not Found
```
❌ Chrome is not installed on your system
```
**Solutions:**
- Verify the application is installed
- FRIDAY checks these locations:
  - `C:\Program Files\Google\Chrome\Application\`
  - `C:\Program Files (x86)\Google\Chrome\Application\`
  - `%LOCALAPPDATA%\Google\Chrome\Application\`
- Try full name: `open google chrome`

#### 5. Screenshot Fails
```
❌ Failed to take screenshot: PyAutoGUI was unable to import pyscreeze
```
**Solution:**
```bash
pip install Pillow
```

#### 6. Permission Denied
```
❌ Permission denied
```
**Solutions:**
- Run as administrator (Windows)
- Check file/folder permissions
- Ensure you own the target directory

### Getting Help

1. Type `help` in FRIDAY for command list
2. Type `mode` to check AI/Local status
3. Check [GITHUB_CHECKLIST.md](GITHUB_CHECKLIST.md) for common issues
4. Run `python check_safety.py` to verify setup

---

## 💰 API Costs & Limits

| Service | Free Tier | Paid | Usage |
|---------|-----------|------|-------|
| **OpenAI GPT-3.5** | $5 credit (new accounts) | ~$0.001-0.003/command | Optional (AI mode) |
| **News API** | 100 requests/day | $449/month | Optional (news feature) |
| **Local Mode** | ∞ Free forever | N/A | Pattern matching |

**Cost Estimate:**
- Local Mode: **$0** (completely free)
- AI Mode: ~$1 for 500-1000 commands
- News: Free for personal use (100/day)

---

## 🤝 Contributing

We welcome contributions! Here's how you can help:

### Before Contributing

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature-name`
3. **Make your changes**
4. **Test thoroughly**:
   - Test both AI and local modes
   - Verify security features work
   - Check edge cases
5. **Run security check**: `python check_safety.py`
6. **Commit your changes**: `git commit -am 'Add feature'`
7. **Push to branch**: `git push origin feature-name`
8. **Submit a pull request**

### Contribution Guidelines

✅ **DO:**
- Follow existing code style
- Add docstrings to functions
- Update README if adding features
- Test on multiple platforms (if possible)
- Keep security as top priority
- Add commands to whitelist only if safe

❌ **DON'T:**
- Commit `.env` file
- Add commands that execute arbitrary code
- Remove security checks
- Bypass user confirmation for risky operations

### Development Setup

```bash
# Clone your fork
git clone https://github.com/your-username/friday.git

# Create virtual environment
python -m venv .venv
.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Make changes and test
python -m friday.main
```

### Running Tests

```bash
# Security check
python check_safety.py

# Manual testing
python -m friday.main
```

---

## 📜 License

This project is provided as-is for **educational and personal use**.

**You may:**
- ✅ Use for personal projects
- ✅ Modify for your needs
- ✅ Learn from the code
- ✅ Share with attribution

**You may NOT:**
- ❌ Use for commercial purposes without permission
- ❌ Remove attribution
- ❌ Hold authors liable for damages

---

## ⚠️ Disclaimer

**Important Notes:**
- Use FRIDAY responsibly and at your own risk
- Test commands in safe directories first
- Review confirmation prompts carefully
- Keep API keys secure and private
- Never commit `.env` to version control
- Authors not responsible for misuse or damages

**Security:**
- FRIDAY uses command whitelisting for security
- System directories are protected
- Risky operations require confirmation
- However, always review commands before confirming

---

## 🎯 Roadmap

### Planned Features
- [ ] Browser automation (Selenium/Playwright)
- [ ] Email integration (send/read)
- [ ] Calendar management
- [ ] Custom automation scripts
- [ ] Plugin system for extensions
- [ ] Voice input/output improvements
- [ ] Multi-language support
- [ ] Mobile app companion
- [ ] Cloud sync for settings
- [ ] Scheduled tasks/automation

### Community Requests
Have an idea? [Open an issue](../../issues) or contribute!

---

## 🙏 Acknowledgments

**Special Thanks:**
- **OpenAI** - GPT API for natural language processing
- **News API** - Free news headlines
- **Python Community** - Amazing open-source libraries

**Built with:**
- Python 3.13
- OpenAI GPT-3.5-Turbo
- PyAutoGUI, psutil, requests, colorama, and more

---

## 📚 Additional Resources

### Documentation
- Type `help` in FRIDAY for command list
- [GITHUB_CHECKLIST.md](GITHUB_CHECKLIST.md) - Pre-commit checklist
- Inline code documentation in all modules

### External Links
- [OpenAI API Documentation](https://platform.openai.com/docs)
- [News API Documentation](https://newsapi.org/docs)
- [Python Official Docs](https://docs.python.org/3/)

### Support
- Report bugs: Open an issue
- Feature requests: Open an issue with [Feature] tag
- Questions: Check existing issues or create new one

---

## 🎉 Quick Tips

1. **Start Simple**: Try `help` first to see all commands
2. **No Quotes**: Type `open chrome`, not `"open chrome"`
3. **Local Mode**: Works without OpenAI (free forever)
4. **Safe by Default**: Risky operations ask for confirmation
5. **Customize**: Edit `friday/config.py` for your preferences

---

**Built with security in mind. AI-powered, human-controlled.** 🤖🔒

Made with ❤️ for Python learners and automation enthusiasts

---

*Last Updated: February 1, 2026*