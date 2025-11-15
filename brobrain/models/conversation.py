from pydantic import Field
from uuid import uuid4
from .base import RoleType, Context, Artifact, BaseBrain
from typing import List, Optional

class Conversation(BaseBrain):
    role:RoleType
    contexts:Optional[List[Context]] = Field(default=None)
    artifacts:Optional[List[Artifact]] = Field(default=None)