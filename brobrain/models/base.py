from pydantic import BaseModel, Field
from typing import Optional
from uuid import uuid4
from datetime import datetime, timezone

class BaseBrain(BaseModel):
    id:str = Field(default_factory=lambda: str(uuid4()))
    model:str
    content:str
    executed_time_ms:Optional[float] = Field(default=0.0)
    input_token:Optional[int] = Field(default=0)
    output_token:Optional[int] = Field(default=0)
    created_at:datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at:datetime = Field(default_factory=lambda: datetime.now(timezone.utc))