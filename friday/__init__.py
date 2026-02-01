"""
FRIDAY - AI-Powered Desktop Automation Assistant

A secure, AI-driven desktop assistant that uses OpenAI to interpret commands
and executes only whitelisted, safe automation functions.
"""

__version__ = "1.0.0"
__author__ = "Your Name"

from friday.ai_brain import ai_brain
from friday.command_parser import command_parser
from friday.config import config

__all__ = ["ai_brain", "command_parser", "config"]
