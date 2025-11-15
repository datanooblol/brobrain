from typing import List, Optional
from enum import StrEnum
from .base import BaseBrain

class EpisodeLevel(StrEnum):
    CONVERSATIONS = "conversations"  # Summarized from conversations
    EPISODES = "episodes"  # Summarized from other episodes

class Episode(BaseBrain):
    vector:List[float]
    conversation_ids:List[str]
    episode_ids:Optional[List[str]] = None  # For tracking parent episodes when summarizing
    session_id:Optional[str] = None
    level:EpisodeLevel = EpisodeLevel.CONVERSATIONS
    is_active:bool = True  # Only active episodes used as context