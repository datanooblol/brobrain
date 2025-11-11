"""
BroBrain Core - Main Memory Management Interface

The main BroBrain class that coordinates all memory operations using
the pluggable backend system. This provides a unified API regardless
of the underlying database backend.
"""

from typing import Dict, Any
from .interfaces import MemoryBackend
from ..working.conversations import ConversationManager
from ..working.episodes import EpisodeManager
from ..knowledge.world import WorldKnowledge
from ..knowledge.sources import SourceManager
from ..execution.procedures import ProcedureManager
from ..execution.states import StateManager

class BroBrain:
    """
    Main BroBrain interface for AI Agent memory management.
    
    Provides a unified API that works with any database backend
    implementing the brobrain protocol interfaces.
    """
    
    def __init__(self, backend: MemoryBackend, config: Dict[str, Any] = None):
        """
        Initialize BroBrain with a specific backend.
        
        Args:
            backend: Database backend implementing MemoryBackend interface
            config: Optional configuration for the backend
        """
        self.backend = backend
        self.backend.connect(config or {})
        
        # Initialize memory managers with the backend
        self.working = WorkingMemory(backend)
        self.knowledge = KnowledgeMemory(backend)
        self.execution = ExecutionMemory(backend)

class WorkingMemory:
    """Working memory operations using the configured backend"""
    
    def __init__(self, backend: MemoryBackend):
        self.conversations = ConversationManager(backend)
        self.episodes = EpisodeManager(backend)

class KnowledgeMemory:
    """Knowledge memory operations using the configured backend"""
    
    def __init__(self, backend: MemoryBackend):
        self.world = WorldKnowledge(backend)
        self.sources = SourceManager(backend)

class ExecutionMemory:
    """Execution memory operations using the configured backend"""
    
    def __init__(self, backend: MemoryBackend):
        self.procedures = ProcedureManager(backend)
        self.states = StateManager(backend)