from pydantic import BaseModel, Field
from uuid import uuid4
from typing import List, Optional
from .base import BaseBrain

class Episode(BaseBrain):
    conversation_ids:List[str]