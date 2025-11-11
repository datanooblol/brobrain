"""
BroBrain Protocol Interfaces - Database-Agnostic Memory Management

Defines abstract interfaces that any database backend can implement.
This allows brobrain to work with DuckDB, PostgreSQL, SQLite, etc.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from datetime import datetime

class MemoryBackend(ABC):
    """Abstract interface for any database backend"""
    
    @abstractmethod
    def connect(self, config: Dict[str, Any]) -> None:
        """Establish database connection"""
        pass
    
    @abstractmethod
    def execute(self, query: str, params: List[Any] = None) -> Any:
        """Execute query with parameters"""
        pass
    
    @abstractmethod
    def fetch_all(self, query: str, params: List[Any] = None) -> List[Dict]:
        """Fetch all results as list of dicts"""
        pass
    
    @abstractmethod
    def fetch_one(self, query: str, params: List[Any] = None) -> Optional[Dict]:
        """Fetch single result as dict"""
        pass

class WorkingMemoryInterface(ABC):
    """Protocol for working memory operations"""
    
    @abstractmethod
    def store_message(self, content: str, role: str, session_id: str) -> str:
        """Store conversation message, return message ID"""
        pass
    
    @abstractmethod
    def get_conversation(self, session_id: str, limit: int = 50) -> List[Dict]:
        """Get conversation history for session"""
        pass
    
    @abstractmethod
    def create_episode(self, session_id: str, summary: str) -> str:
        """Create episode summary, return episode ID"""
        pass

class KnowledgeInterface(ABC):
    """Protocol for external knowledge operations"""
    
    @abstractmethod
    def store_knowledge(self, content: str, source: str, metadata: Dict) -> str:
        """Store external knowledge, return knowledge ID"""
        pass
    
    @abstractmethod
    def search_knowledge(self, query: str, limit: int = 10) -> List[Dict]:
        """Search knowledge base"""
        pass

class ExecutionInterface(ABC):
    """Protocol for AI execution state operations"""
    
    @abstractmethod
    def update_state(self, agent_id: str, state: str, metadata: Dict) -> None:
        """Update agent state"""
        pass
    
    @abstractmethod
    def get_current_state(self, agent_id: str) -> Optional[Dict]:
        """Get current agent state"""
        pass