from novelinsights.types.base import DescribedEnum

from typing import Type

class PromptType(DescribedEnum):
    BASE = ("base", "Base prompt type")
    SUMMARIZE_CHAPTER = ("summarize_chapter", "Summarize a chapter of a book")
    FIND_ENTITIES = ("find_entities", "Find all narratively significant entities from a chapter of a book")
    UPSERT_ENTITIES = ("upsert_entities", "Update or create the entities in a chapter of a book")
    
    def get_prompt_class(self) -> Type:
        """Get the prompt class for this type"""
        from novelinsights.services.ai.prompts import SummarizeChapterPrompt
        from novelinsights.services.ai.prompts import FindEntitiesPrompt
        from novelinsights.services.ai.prompts import UpsertEntitiesPrompt
        
        prompt_map = {
            PromptType.SUMMARIZE_CHAPTER: SummarizeChapterPrompt,
            PromptType.FIND_ENTITIES: FindEntitiesPrompt,
            PromptType.UPSERT_ENTITIES: UpsertEntitiesPrompt,
        }
        return prompt_map[self]
