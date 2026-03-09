"""
AutoDev Factory Agents Module

This module contains all the AI agents that power the AutoDev Factory system.
"""

from .base_agent import BaseAgent, AgentState, AgentResult
from .trend_research_agent import TrendResearchAgent
from .niche_finder_agent import NicheFinderAgent
from .idea_generator_agent import IdeaGeneratorAgent
from .product_manager_agent import ProductManagerAgent
from .system_architect_agent import SystemArchitectAgent
from .file_structure_agent import FileStructureAgent
from .code_generator_agent import CodeGeneratorAgent
from .testing_agent import TestingAgent
from .debug_agent import DebugAgent
from .documentation_agent import DocumentationAgent
from .github_agent import GitHubAgent
from .deployment_agent import DeploymentAgent
from .security_agent import SecurityAgent
from .optimization_agent import OptimizationAgent
from .learning_agent import LearningAgent

__all__ = [
    "BaseAgent",
    "AgentState",
    "AgentResult",
    "TrendResearchAgent",
    "NicheFinderAgent",
    "IdeaGeneratorAgent",
    "ProductManagerAgent",
    "SystemArchitectAgent",
    "FileStructureAgent",
    "CodeGeneratorAgent",
    "TestingAgent",
    "DebugAgent",
    "DocumentationAgent",
    "GitHubAgent",
    "DeploymentAgent",
    "SecurityAgent",
    "OptimizationAgent",
    "LearningAgent",
]
