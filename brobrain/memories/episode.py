from brobrain.models.episode import Episode
from .duck_base import DuckBase
from typing import Optional

class DuckEpisode(DuckBase):
    def __init__(self, vector_size: int, db_path: Optional[str] = None):
        super().__init__(Episode, "episodes", db_path)
        self.vector_size = vector_size
        self.init_database()

    def init_database(self)->None:
        query = f"""
        CREATE TABLE IF NOT EXISTS episodes (
            id VARCHAR PRIMARY KEY,
            model VARCHAR NOT NULL,
            content VARCHAR NOT NULL,
            executed_time_ms DOUBLE DEFAULT 0,
            input_token INTEGER DEFAULT 0,
            output_token INTEGER DEFAULT 0,
            vector FLOAT[{self.vector_size}],
            conversation_ids JSON NOT NULL,
            episode_ids JSON DEFAULT NULL,
            session_id VARCHAR DEFAULT NULL,
            level VARCHAR CHECK (level IN ('conversations', 'episodes')) DEFAULT 'conversations',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        self.execute(query, None)
