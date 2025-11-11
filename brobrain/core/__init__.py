"""
Core Module - Shared Infrastructure

Provides shared utilities, database connections, and common functionality
used across all brobrain modules.

Components:
- database: DuckDB connection and query management
- models: Pydantic models for data validation
- utils: Common utilities and helper functions
"""

from .database import DatabaseManager
from .models import *
from .utils import *

__all__ = ["DatabaseManager"]