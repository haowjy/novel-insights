from novelinsights.types.base import DescribedEnum

from typing import Type

class PromptType(DescribedEnum):
    BASE = ("base", "Base prompt type")
    SUMMARIZE_CHAPTER = ("summarize_chapter", "Summarize a chapter of a book")
    FIND_ENTITIES = ("find_entities", "Find all narratively significant entities from a chapter of a book")
    
    def get_prompt_class(self) -> Type:
        """Get the prompt class for this type"""
        from novelinsights.services.ai.prompts.narrative.chapterbychapter.summarize import SummarizeChapterPrompt
        from novelinsights.services.ai.prompts.narrative.chapterbychapter.find_entities import FindEntitiesPrompt
        prompt_map = {
            PromptType.SUMMARIZE_CHAPTER: SummarizeChapterPrompt,
            PromptType.FIND_ENTITIES: FindEntitiesPrompt,
        }
        return prompt_map[self]
