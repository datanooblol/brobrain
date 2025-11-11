"""
Knowledge Module - Outside Brain

Manages external knowledge sources that exist independently of AI interactions.
This is the "world knowledge" that the AI can access but doesn't inherently understand
until it interacts with it and brings it into working memory.

Components:
- world: External knowledge sources (RAG, APIs, databases)
- sources: File systems, search engines, and data connectors
"""

from .world import WorldKnowledge
from .sources import SourceManager

__all__ = ["WorldKnowledge", "SourceManager"]