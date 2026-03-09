"""
Workflow Engine for AutoDev Factory

This module provides the workflow execution engine.
"""

from typing import Dict, Any, List, Callable
import logging

logger = logging.getLogger(__name__)


class WorkflowEngine:
    """
    Generic workflow engine for executing multi-step processes.
    """
    
    def __init__(self):
        self.steps = []
        self.context = {}
    
    def add_step(self, name: str, func: Callable, dependencies: List[str] = None):
        """Add a step to the workflow."""
        self.steps.append({
            'name': name,
            'func': func,
            'dependencies': dependencies or []
        })
    
    async def execute(self, initial_context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Execute the workflow."""
        self.context = initial_context or {}
        
        for step in self.steps:
            logger.info(f"Executing step: {step['name']}")
            try:
                result = await step['func'](self.context)
                self.context[step['name']] = result
            except Exception as e:
                logger.error(f"Step {step['name']} failed: {str(e)}")
                raise
        
        return self.context
