"""
Working Memory Module - Inside Brain

Manages active memory that exists only during user-AI interactions.
This is the "conscious" memory that the AI is actively using and processing.

Components:
- conversations: Live dialogue tracking between user and AI
- episodes: Summarized interaction rounds for episodic memory
"""

from .conversations import ConversationManager
from .episodes import EpisodeManager

__all__ = ["ConversationManager", "EpisodeManager"]