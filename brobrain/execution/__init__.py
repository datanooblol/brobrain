"""
Execution Module - AI Brain

Manages the AI agent's internal state, procedures, and workflow tracking.
This is the "metacognitive" layer that tracks what the AI is doing and planning.

Components:
- procedures: Current task execution and workflow management
- states: AI agent state tracking and decision history
"""

from .procedures import ProcedureManager
from .states import StateManager

__all__ = ["ProcedureManager", "StateManager"]