from brobrain.models.conversation import Conversation
from .duck_base import DuckBase
from typing import Optional

class DuckConversation(DuckBase):
    """DuckDB-based conversation memory storage for LLM interactions.
    
    Provides persistent storage and retrieval of conversation data using DuckDB.
    Automatically manages database schema with timestamps and supports CRUD operations.
    
    Args:
        db_path (Optional[str]): Path to DuckDB file. Defaults to "brobrain.db".
    
    Examples:
        Basic usage:
        >>> dc = DuckConversation()
        >>> dc.create(conversation)
        >>> conversations = dc.read()
        
        Query by ID or session:
        >>> conversation = dc.read(id="some-id")
        >>> session_conversations = dc.read(session_id="session-123")
        
        Update conversation metadata:
        >>> dc.update(id="some-id", input_token=100, output_token=200)
        
        Delete conversations:
        >>> dc.delete(id="some-id")
        >>> dc.delete(session_id="session-123")
    """
    def __init__(self, db_path: Optional[str] = None):
        super().__init__(Conversation, "conversations", db_path)
        self.init_database()


    def init_database(self)->None:
        query = """
        CREATE TABLE IF NOT EXISTS conversations (
            id VARCHAR PRIMARY KEY,
            model VARCHAR NOT NULL,
            content VARCHAR NOT NULL,
            role VARCHAR CHECK (role IN ('user', 'assistant')) NOT NULL,
            executed_time_ms DOUBLE DEFAULT 0,
            input_token INTEGER DEFAULT 0,
            output_token INTEGER DEFAULT 0,
            contexts JSON DEFAULT NULL,
            artifacts JSON DEFAULT NULL,
            session_id VARCHAR DEFAULT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        self.execute(query, None)
    

    
