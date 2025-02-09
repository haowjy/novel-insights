from typing import Any

from novelinsights.services.ai.prompts.narrative.mixins import NarrativeExtractionMixin
from novelinsights.services.ai.prompts.base import PromptBase

class ExtractChapterKnowledgePrompt(NarrativeExtractionMixin, PromptBase):
    """Prompt for extracting knowledge from a chapter of a book"""
    
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
    
    