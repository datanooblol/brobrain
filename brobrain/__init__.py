"""
BroBrain - AI Agent Memory Management Library

A protocol-based library for managing AI agent memory across three core domains:
- working: Active memory during user-AI interactions
- knowledge: External knowledge sources and world data
- execution: AI agent state and procedure tracking

Usage:
    from brobrain import BroBrain
    from brobrain.backends import DuckDBBackend
    
    # Initialize with DuckDB backend
    brain = BroBrain(backend=DuckDBBackend())
    
    # Store conversation
    brain.working.store_message("Hello", "user", "session_123")
    
    # Future: Switch to PostgreSQL
    # brain = BroBrain(backend=PostgreSQLBackend("postgresql://..."))
"""

from .core.brain import BroBrain
from . import backends

__version__ = "0.1.0"
__all__ = ["BroBrain", "backends"]