"""
DuckDB Backend Implementation

Implements the brobrain protocol interfaces using DuckDB as the storage backend.
Provides fast analytical queries and embedded database functionality.
"""

import duckdb
from typing import List, Dict, Any, Optional
from ..core.interfaces import MemoryBackend, WorkingMemoryInterface, KnowledgeInterface, ExecutionInterface

class DuckDBBackend(MemoryBackend):
    """DuckDB implementation of the brobrain memory protocol"""
    
    def __init__(self, db_path: str = ":memory:"):
        self.db_path = db_path
        self.conn = None
    
    def connect(self, config: Dict[str, Any] = None) -> None:
        """Establish DuckDB connection"""
        self.conn = duckdb.connect(self.db_path)
        self._initialize_schema()
    
    def execute(self, query: str, params: List[Any] = None) -> Any:
        """Execute query with parameters"""
        if params:
            return self.conn.execute(query, params)
        return self.conn.execute(query)
    
    def fetch_all(self, query: str, params: List[Any] = None) -> List[Dict]:
        """Fetch all results as list of dicts"""
        result = self.execute(query, params)
        return [dict(zip([col[0] for col in result.description], row)) for row in result.fetchall()]
    
    def fetch_one(self, query: str, params: List[Any] = None) -> Optional[Dict]:
        """Fetch single result as dict"""
        results = self.fetch_all(query, params)
        return results[0] if results else None
    
    def _initialize_schema(self):
        """Create brobrain tables if they don't exist"""
        # Working memory tables
        self.execute("""
            CREATE TABLE IF NOT EXISTS conversations (
                id VARCHAR(36) PRIMARY KEY,
                content TEXT NOT NULL,
                role VARCHAR(20) NOT NULL,
                session_id VARCHAR(36) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Knowledge tables
        self.execute("""
            CREATE TABLE IF NOT EXISTS knowledge_items (
                id VARCHAR(36) PRIMARY KEY,
                content TEXT NOT NULL,
                source VARCHAR(255) NOT NULL,
                metadata JSON,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Execution tables
        self.execute("""
            CREATE TABLE IF NOT EXISTS agent_states (
                agent_id VARCHAR(36) NOT NULL,
                state VARCHAR(50) NOT NULL,
                metadata JSON,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (agent_id, created_at)
            )
        """)