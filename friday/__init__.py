"""
FRIDAY - secure tool-using AI desktop assistant.
"""

__version__ = "2.0.0"

from friday.agent import assistant_agent
from friday.ai_brain import ai_brain
from friday.config import config

__all__ = ["assistant_agent", "ai_brain", "config"]
