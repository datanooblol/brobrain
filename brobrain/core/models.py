"""
BroBrain Data Models - Standardized Contracts

Defines Pydantic models that serve as contracts between brobrain and any database backend.
These models ensure consistent data structure regardless of the underlying storage.

All backends must handle these exact data structures.
"""

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, Dict, Any, List
from enum import Enum

class MessageRole(str, Enum):
    """Standardized message roles"""
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"

class Message(BaseModel):
    """Individual conversation message - Working Memory Contract"""
    id: str = Field(..., description="Unique message identifier")
    content: str = Field(..., description="Message content")
    role: MessageRole = Field(..., description="Message role (user/assistant/system)")
    session_id: str = Field(..., description="Session identifier")
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    metadata: Optional[Dict[str, Any]] = Field(default=None, description="Additional metadata")

class Episode(BaseModel):
    """Episodic memory summary - Working Memory Contract"""
    id: str = Field(..., description="Unique episode identifier")
    session_id: str = Field(..., description="Related session identifier")
    summary: str = Field(..., description="Episode summary")
    key_topics: List[str] = Field(default_factory=list, description="Key topics discussed")
    message_count: int = Field(..., description="Number of messages in episode")
    created_at: datetime = Field(default_factory=datetime.now)
    metadata: Optional[Dict[str, Any]] = Field(default=None)

class KnowledgeItem(BaseModel):
    """External knowledge entry - Knowledge Memory Contract"""
    id: str = Field(..., description="Unique knowledge identifier")
    content: str = Field(..., description="Knowledge content")
    source: str = Field(..., description="Knowledge source (file, API, etc.)")
    source_type: str = Field(..., description="Type of source (file, web, database)")
    embedding: Optional[List[float]] = Field(default=None, description="Vector embedding")
    created_at: datetime = Field(default_factory=datetime.now)
    metadata: Optional[Dict[str, Any]] = Field(default=None)

class AgentState(BaseModel):
    """AI agent state snapshot - Execution Memory Contract"""
    agent_id: str = Field(..., description="Agent identifier")
    state: str = Field(..., description="Current state (idle, thinking, responding)")
    procedure_id: Optional[str] = Field(default=None, description="Current procedure ID")
    created_at: datetime = Field(default_factory=datetime.now)
    metadata: Optional[Dict[str, Any]] = Field(default=None)

class Procedure(BaseModel):
    """Task execution record - Execution Memory Contract"""
    id: str = Field(..., description="Unique procedure identifier")
    agent_id: str = Field(..., description="Agent executing the procedure")
    name: str = Field(..., description="Procedure name")
    status: str = Field(..., description="Status (pending, running, completed, failed)")
    started_at: datetime = Field(default_factory=datetime.now)
    completed_at: Optional[datetime] = Field(default=None)
    result: Optional[Dict[str, Any]] = Field(default=None, description="Procedure result")
    metadata: Optional[Dict[str, Any]] = Field(default=None)