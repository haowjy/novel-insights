from typing import Any, TypedDict
from packaging.version import Version

from novelinsights.services.ai.prompts.narrative.mixins import NarrativeExtractionMixin
from novelinsights.services.ai.prompts.base import PromptBase
from novelinsights.types.services.prompt import PromptType

class SummarizeChapterPromptParams(TypedDict):
    chapter_id: str
    genres: list[str]
    chapter_title: str 
    chapter_content: str # preferred format: markdown
    
class SummarizeChapterPrompt(NarrativeExtractionMixin, PromptBase):
    """Prompt for reading a chapter of a book"""
    
    def __init__(
        self, 
        *args: Any, 
        **kwargs: Any
    ) -> None:
        super().__init__(*args, **kwargs)
    
    @property
    def name(self) -> str:
        return "summarize_chapter"
    
    @property
    def version(self) -> Version:
        return Version("0.0.1")
    
    @property
    def type(self) -> PromptType:
        return PromptType.SUMMARIZE_CHAPTER
    
    @property
    def description(self) -> str:
        return "Summarize a chapter of a book"
    