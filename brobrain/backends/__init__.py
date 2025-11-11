"""
Database Backends - Implementation of BroBrain Protocol

Different database implementations that follow the brobrain protocol interfaces.
Each backend provides the same API but uses different underlying storage.

Available Backends:
- DuckDBBackend: Fast analytical queries, embedded database
- PostgreSQLBackend: Production-ready, ACID compliance
- SQLiteBackend: Lightweight, file-based storage
"""

from .base_backend import BaseBackend
from .duckdb_backend import DuckDBBackend

__all__ = ["BaseBackend", "DuckDBBackend"]