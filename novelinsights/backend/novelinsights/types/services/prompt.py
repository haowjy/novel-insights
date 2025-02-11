from novelinsights.types.base import DescribedEnum

from typing import Type

class PromptType(DescribedEnum):
    BASE = ("base", "Base prompt type")
    SUMMARIZE_CHAPTER = ("summarize_chapter", "Summarize a chapter of a book")
    EXTRACT_CHAPTER_KNOWLEDGE = ("extract_chapter_knowledge", "Extract knowledge from a chapter of a book")
    
    def get_prompt_class(self) -> Type:
        """Get the prompt class for this type"""
        from novelinsights.services.ai.prompts.narrative.chapterbychapter.summarize import SummarizeChapterPrompt
        
        prompt_map = {
            PromptType.SUMMARIZE_CHAPTER: SummarizeChapterPrompt,
        }
        return prompt_map[self]
