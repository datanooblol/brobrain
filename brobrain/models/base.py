from pydantic import BaseModel, Field
from enum import StrEnum
from typing import Optional
from uuid import uuid4

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

class BaseBrain(BaseModel):
    id:str = Field(default_factory=lambda: str(uuid4()))
    model:str
    content:str
    executed_time_ms:Optional[float] = Field(default=0.0)
    input_token:Optional[int] = Field(default=0)
    output_token:Optional[int] = Field(default=0)