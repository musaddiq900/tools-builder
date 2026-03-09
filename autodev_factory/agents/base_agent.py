"""
Base Agent Class for AutoDev Factory

This module defines the abstract base class for all agents in the system.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field
from enum import Enum
import time
import logging

logger = logging.getLogger(__name__)


class AgentState(str, Enum):
    """Possible states for an agent."""
    IDLE = "idle"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    WAITING = "waiting"


class AgentResult(BaseModel):
    """Result returned by an agent after execution."""
    
    success: bool = Field(..., description="Whether the agent execution was successful")
    data: Any = Field(default=None, description="Data returned by the agent")
    message: str = Field(default="", description="Status message or error message")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")
    execution_time: float = Field(default=0.0, description="Execution time in seconds")
    
    class Config:
        arbitrary_types_allowed = True


class BaseAgent(ABC, BaseModel):
    """
    Abstract base class for all agents in the AutoDev Factory system.
    
    All agents must inherit from this class and implement the execute method.
    """
    
    name: str = Field(..., description="Name of the agent")
    description: str = Field(default="", description="Description of what the agent does")
    state: AgentState = Field(default=AgentState.IDLE, description="Current state of the agent")
    max_retries: int = Field(default=3, description="Maximum number of retries on failure")
    timeout: int = Field(default=300, description="Timeout in seconds")
    
    class Config:
        arbitrary_types_allowed = True
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._execution_history: List[Dict[str, Any]] = []
    
    @abstractmethod
    async def execute(self, input_data: Dict[str, Any]) -> AgentResult:
        """
        Execute the agent's main logic.
        
        Args:
            input_data: Input data required by the agent
            
        Returns:
            AgentResult with success status and output data
        """
        pass
    
    async def run(self, input_data: Dict[str, Any]) -> AgentResult:
        """
        Run the agent with retry logic and error handling.
        
        Args:
            input_data: Input data for the agent
            
        Returns:
            AgentResult with execution outcome
        """
        self.state = AgentState.RUNNING
        start_time = time.time()
        
        last_error = None
        
        for attempt in range(self.max_retries):
            try:
                logger.info(f"Running agent '{self.name}' (attempt {attempt + 1}/{self.max_retries})")
                
                result = await self.execute(input_data)
                
                if result.success:
                    result.execution_time = time.time() - start_time
                    self.state = AgentState.SUCCESS
                    self._log_execution(input_data, result, attempt)
                    return result
                else:
                    last_error = result.message
                    logger.warning(f"Agent '{self.name}' failed: {result.message}")
                    
            except Exception as e:
                last_error = str(e)
                logger.error(f"Agent '{self.name}' encountered an error: {str(e)}", exc_info=True)
            
            if attempt < self.max_retries - 1:
                # Wait before retrying (exponential backoff)
                wait_time = min(2 ** attempt, 30)  # Max 30 seconds between retries
                logger.info(f"Retrying in {wait_time} seconds...")
                await asyncio.sleep(wait_time)
        
        # All retries exhausted
        self.state = AgentState.FAILED
        execution_time = time.time() - start_time
        
        result = AgentResult(
            success=False,
            message=f"Agent failed after {self.max_retries} attempts. Last error: {last_error}",
            execution_time=execution_time
        )
        
        self._log_execution(input_data, result, self.max_retries - 1)
        return result
    
    def _log_execution(self, input_data: Dict[str, Any], result: AgentResult, attempt: int):
        """Log execution history."""
        self._execution_history.append({
            "timestamp": time.time(),
            "attempt": attempt + 1,
            "input": input_data,
            "success": result.success,
            "message": result.message,
            "execution_time": result.execution_time
        })
    
    def get_execution_history(self) -> List[Dict[str, Any]]:
        """Get the execution history of the agent."""
        return self._execution_history
    
    def reset(self):
        """Reset the agent to its initial state."""
        self.state = AgentState.IDLE
        self._execution_history = []
    
    def get_status(self) -> Dict[str, Any]:
        """Get current status of the agent."""
        return {
            "name": self.name,
            "description": self.description,
            "state": self.state.value,
            "execution_count": len(self._execution_history),
            "last_execution": self._execution_history[-1] if self._execution_history else None
        }


# Import asyncio for retry logic
import asyncio
