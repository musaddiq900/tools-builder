"""
AutoDev Factory Agents Module

This module contains all the AI agents that power the AutoDev Factory system.
"""

from .base_agent import BaseAgent, AgentState, AgentResult
from .trend_research_agent import TrendResearchAgent
from .niche_finder_agent import NicheFinderAgent

__all__ = [
    "BaseAgent",
    "AgentState",
    "AgentResult",
    "TrendResearchAgent",
    "NicheFinderAgent",
]
