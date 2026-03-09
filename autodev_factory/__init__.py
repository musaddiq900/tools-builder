"""
AutoDev Factory - Complete Autonomous AI Developer Agent System

This is the main package initialization file.
"""

__version__ = "1.0.0"
__author__ = "AutoDev Factory Team"
__description__ = "Fully Autonomous AI Developer Agent that builds software tools automatically"

from .agents.base_agent import BaseAgent
from .core.orchestrator import Orchestrator
from .config.settings import Settings

__all__ = [
    "BaseAgent",
    "Orchestrator", 
    "Settings",
]