import duckdb
from typing import Optional, Any, Type, TypeVar
from pydantic import BaseModel
from .base import BaseMemory

T = TypeVar('T', bound=BaseModel)

class DuckBase(BaseMemory):
    def __init__(self, model_class: Type[T], table_name: str, db_path: Optional[str] = None):
        self.model_class = model_class
        self.table_name = table_name
        self.db_path = db_path if db_path else "brobrain.db"
    
    def execute(self, query: str, data: Optional[Any] = None):
        with duckdb.connect(self.db_path) as conn:
            return conn.execute(query, data).df()
    
    def _df_to_models(self, df):
        models = []
        for _, row in df.iterrows():
            data = row.to_dict()
            models.append(self.model_class(**data))
        return models
    
    def create(self, model: T):
        data = model.model_dump()
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['?' for _ in data])
        query = f"INSERT INTO {self.table_name} ({columns}) VALUES ({placeholders})"
        return self.execute(query, tuple(data.values()))
    
    def read(self, id: Optional[str] = None, session_id: Optional[str] = None, limit: Optional[int] = None, order_asc: bool = True, as_model: bool = True):
        if id:
            query = f"SELECT * FROM {self.table_name} WHERE id = ?"
            df = self.execute(query, (id,))
        elif session_id:
            query = f"SELECT * FROM {self.table_name} WHERE session_id = ?"
            df = self.execute(query, (session_id,))
        else:
            query = f"SELECT * FROM {self.table_name}"
            if order_asc:
                query += " ORDER BY created_at ASC"
            else:
                query += " ORDER BY created_at DESC"
            if limit:
                query += f" LIMIT {limit}"
            df = self.execute(query)
        
        return self._df_to_models(df) if as_model else df
    
    def update(self, id: str, **fields):
        set_clause = ', '.join([f"{k} = ?" for k in fields.keys()])
        query = f"UPDATE {self.table_name} SET {set_clause}, updated_at = CURRENT_TIMESTAMP WHERE id = ?"
        return self.execute(query, tuple(fields.values()) + (id,))
    
    def delete(self, id: Optional[str] = None, session_id: Optional[str] = None):
        if id:
            query = f"DELETE FROM {self.table_name} WHERE id = ?"
            return self.execute(query, (id,))
        elif session_id:
            query = f"DELETE FROM {self.table_name} WHERE session_id = ?"
            return self.execute(query, (session_id,))