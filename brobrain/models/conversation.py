from pydantic import Field
from .base import BaseBrain
from typing import List, Optional
from enum import StrEnum
from pydantic import BaseModel

class RoleType(StrEnum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"

class ContextType(StrEnum):
    DATA = "data"
    KG = "kg"
    MEMORY = "memory"

class ArtifactType(StrEnum):
    SQL = "sql"
    PYTHON = "python"
    DATA = "data"
    CHART = "chart"

class Context(BaseModel):
    type:ContextType
    content:str

class Artifact(BaseModel):
    type:ArtifactType
    content:str
    title:str

class Conversation(BaseBrain):
    role:RoleType = Field(default=RoleType.USER)
    contexts:Optional[List[Context]] = Field(default=None)
    artifacts:Optional[List[Artifact]] = Field(default=None)
    session_id:Optional[str] = Field(default=None)