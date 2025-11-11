"""
Base Backend - Foundation for Custom Database Implementations

Provides a base class that users can extend to create their own database backends.
Includes common functionality and enforces the brobrain protocol contracts.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from ..core.interfaces import MemoryBackend
from ..core.models import Message, Episode, KnowledgeItem, AgentState, Procedure

class BaseBackend(MemoryBackend):
    """
    Base backend class that provides common functionality for all database implementations.
    
    Users can extend this class to create custom backends for any database system.
    All methods work with standardized brobrain data models as contracts.
    """
    
    def __init__(self, connection_config: Dict[str, Any] = None):
        """Initialize backend with connection configuration"""
        self.connection_config = connection_config or {}
        self.is_connected = False
    
    @abstractmethod
    def connect(self, config: Dict[str, Any] = None) -> None:
        """Establish database connection - must be implemented by subclasses"""
        pass
    
    @abstractmethod
    def execute(self, query: str, params: List[Any] = None) -> Any:
        """Execute raw query - must be implemented by subclasses"""
        pass
    
    @abstractmethod
    def fetch_all(self, query: str, params: List[Any] = None) -> List[Dict]:
        """Fetch all results - must be implemented by subclasses"""
        pass
    
    @abstractmethod
    def fetch_one(self, query: str, params: List[Any] = None) -> Optional[Dict]:
        """Fetch single result - must be implemented by subclasses"""
        pass
    
    # High-level operations using standardized models
    def store_message(self, message: Message) -> str:
        """Store message using Message contract"""
        return self._store_message_impl(message)
    
    def get_messages(self, session_id: str, limit: int = 50) -> List[Message]:
        """Get messages using Message contract"""
        data = self._get_messages_impl(session_id, limit)
        return [Message(**row) for row in data]
    
    def store_episode(self, episode: Episode) -> str:
        """Store episode using Episode contract"""
        return self._store_episode_impl(episode)
    
    def store_knowledge(self, knowledge: KnowledgeItem) -> str:
        """Store knowledge using KnowledgeItem contract"""
        return self._store_knowledge_impl(knowledge)
    
    def update_agent_state(self, state: AgentState) -> None:
        """Update agent state using AgentState contract"""
        self._update_agent_state_impl(state)
    
    def store_procedure(self, procedure: Procedure) -> str:
        """Store procedure using Procedure contract"""
        return self._store_procedure_impl(procedure)
    
    # Abstract methods that subclasses must implement for each data type
    @abstractmethod
    def _store_message_impl(self, message: Message) -> str:
        """Implementation-specific message storage"""
        pass
    
    @abstractmethod
    def _get_messages_impl(self, session_id: str, limit: int) -> List[Dict]:
        """Implementation-specific message retrieval"""
        pass
    
    @abstractmethod
    def _store_episode_impl(self, episode: Episode) -> str:
        """Implementation-specific episode storage"""
        pass
    
    @abstractmethod
    def _store_knowledge_impl(self, knowledge: KnowledgeItem) -> str:
        """Implementation-specific knowledge storage"""
        pass
    
    @abstractmethod
    def _update_agent_state_impl(self, state: AgentState) -> None:
        """Implementation-specific state update"""
        pass
    
    @abstractmethod
    def _store_procedure_impl(self, procedure: Procedure) -> str:
        """Implementation-specific procedure storage"""
        pass
    
    def validate_connection(self) -> bool:
        """Check if backend is properly connected"""
        return self.is_connected
    
    def close(self) -> None:
        """Close database connection - can be overridden by subclasses"""
        self.is_connected = False