from typing import Any, TypedDict
from packaging.version import Version

from novelinsights.services.ai.prompts.narrative.mixins import NarrativeExtractionMixin
from novelinsights.services.ai.prompts.base import PromptBase
from novelinsights.types.services.prompt import PromptType

class ReadChapterPromptParams(TypedDict):
    chapter_id: str

class ReadChapterPrompt(NarrativeExtractionMixin, PromptBase):
    """Prompt for reading a chapter of a book"""
    
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
    
    @property
    def name(self) -> str:
        return "read_chapter"
    
    @property
    def version(self) -> Version:
        return Version("0.0.1")
    
    @property
    def type(self) -> PromptType:
        return PromptType.READ_CHAPTER
    
    @property
    def description(self) -> str:
        return "Read a chapter of a book"
    