"""
Example: Creating a Custom Backend for BroBrain

This example shows how users can create their own database backend
by extending BaseBackend and implementing the required methods.
"""

from brobrain.backends import BaseBackend
from brobrain.core.models import Message, Episode, KnowledgeItem, AgentState, Procedure
from typing import List, Dict, Any, Optional
import sqlite3
import json

class SQLiteBackend(BaseBackend):
    """
    Example custom backend using SQLite.
    
    Users can follow this pattern to create backends for:
    - MongoDB
    - Redis
    - Cassandra
    - Any other database system
    """
    
    def __init__(self, db_path: str = ":memory:"):
        super().__init__({"db_path": db_path})
        self.db_path = db_path
        self.conn = None
    
    def connect(self, config: Dict[str, Any] = None) -> None:
        """Establish SQLite connection"""
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row  # Return rows as dicts
        self._create_tables()
        self.is_connected = True
    
    def execute(self, query: str, params: List[Any] = None) -> Any:
        """Execute SQLite query"""
        cursor = self.conn.cursor()
        if params:
            return cursor.execute(query, params)
        return cursor.execute(query)
    
    def fetch_all(self, query: str, params: List[Any] = None) -> List[Dict]:
        """Fetch all results as list of dicts"""
        cursor = self.execute(query, params)
        return [dict(row) for row in cursor.fetchall()]
    
    def fetch_one(self, query: str, params: List[Any] = None) -> Optional[Dict]:
        """Fetch single result as dict"""
        cursor = self.execute(query, params)
        row = cursor.fetchone()
        return dict(row) if row else None
    
    def _create_tables(self):
        """Create SQLite tables matching brobrain contracts"""
        self.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id TEXT PRIMARY KEY,
                content TEXT NOT NULL,
                role TEXT NOT NULL,
                session_id TEXT NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                metadata TEXT
            )
        """)
        
        self.execute("""
            CREATE TABLE IF NOT EXISTS episodes (
                id TEXT PRIMARY KEY,
                session_id TEXT NOT NULL,
                summary TEXT NOT NULL,
                key_topics TEXT,
                message_count INTEGER NOT NULL,
                created_at TEXT NOT NULL,
                metadata TEXT
            )
        """)
        
        # Add other tables for knowledge, states, procedures...
        self.conn.commit()
    
    def _store_message_impl(self, message: Message) -> str:
        """Store message in SQLite"""
        self.execute("""
            INSERT INTO messages (id, content, role, session_id, created_at, updated_at, metadata)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, [
            message.id, message.content, message.role.value, message.session_id,
            message.created_at.isoformat(), message.updated_at.isoformat(),
            json.dumps(message.metadata) if message.metadata else None
        ])
        self.conn.commit()
        return message.id
    
    def _get_messages_impl(self, session_id: str, limit: int) -> List[Dict]:
        """Get messages from SQLite"""
        return self.fetch_all("""
            SELECT * FROM messages 
            WHERE session_id = ? 
            ORDER BY created_at DESC 
            LIMIT ?
        """, [session_id, limit])
    
    # Implement other required methods...
    def _store_episode_impl(self, episode: Episode) -> str:
        # Implementation for episodes
        pass
    
    def _store_knowledge_impl(self, knowledge: KnowledgeItem) -> str:
        # Implementation for knowledge
        pass
    
    def _update_agent_state_impl(self, state: AgentState) -> None:
        # Implementation for agent states
        pass
    
    def _store_procedure_impl(self, procedure: Procedure) -> str:
        # Implementation for procedures
        pass

# Usage example:
if __name__ == "__main__":
    from brobrain import BroBrain
    
    # Use custom SQLite backend
    custom_backend = SQLiteBackend("my_brain.db")
    brain = BroBrain(backend=custom_backend)
    
    # Same API works with any backend!
    brain.working.conversations.store_message("Hello", "user", "session_123")