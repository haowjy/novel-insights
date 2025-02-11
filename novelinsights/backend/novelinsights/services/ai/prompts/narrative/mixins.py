# novelinsights/services/ai/prompts/narrative/mixins.py

from dataclasses import dataclass
from typing import Any, Optional

@dataclass
class NarrativeStoryMixin:
    """Mixin for prompts that extract narrative information from a book
    Includes story metadata from the book
    """
    
    story_title: str
    story_description: Optional[str]
    genres: Optional[list[str]]
    additional_tags: Optional[list[str]]
    
    def has_story_metadata(self) -> bool:
        return bool(self.story_title or self.genres or self.additional_tags or self.story_description)

    def _persona(self) -> str:
        return (
            "# Persona\n"
            "You are an expert Narrative Knowledge Assistant, combining the skills of a literary analyst, teacher, and storytelling guide."
        )
    
    def _overarching_goal(self) -> str:
        return (
            "# Overarching Goal\n"
            "Extract and structure knowledge from the narrative while maintaining proper story progression context and preventing spoilers."
        )

@dataclass
class NarrativeChapterMixin:
    """Mixin for prompts that extract narrative information from a book
    Includes chapter metadata from the book
    """
    
    chapter_title: str
    chapter_content: str
    
    def has_chapter_data(self) -> bool:
        return bool(self.chapter_title and self.chapter_content)
    
    