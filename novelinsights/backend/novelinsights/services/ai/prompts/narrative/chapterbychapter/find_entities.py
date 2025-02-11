from typing import Any, Optional
from dataclasses import dataclass

from novelinsights.core.config import ModelConfig
from novelinsights.services.ai.prompts.narrative.mixins import NarrativeChapterMixin, NarrativeStoryMixin
from novelinsights.services.ai.prompts.base import PromptBase, PromptTemplateBase
from novelinsights.types.knowledge import EntityType
from novelinsights.types.services.prompt import PromptType
from novelinsights.types.services.provider import Provider

@dataclass
class FindEntitiesTemplate(NarrativeStoryMixin, NarrativeChapterMixin, PromptTemplateBase):
    
    # Summaries of the story so far
    story_summary: Optional[str] = None # summary of the entire story so far
    last_n_chapters_summary: Optional[str] = None # concatenate the summaries of the last n chapters
    
    is_structured_output: bool = True # whether to use structured output offered by openAI or gemini so far 2025-10-02
    
    def has_story_summaries(self) -> bool:
        return bool(self.story_summary or self.last_n_chapters_summary)

    def prompt(self, **kwargs: Any) -> str:
        # update prompt config with kwargs
        self.update(**kwargs)
        
        has_story_metadata = self.has_story_metadata()
        has_chapter_data = self.has_chapter_data()
        has_story_summaries = self.has_story_summaries()
        
        p = (
            f"{self._persona()}\n\n" +
            "# Overarching Goal\n" +
            f"Extract all narratively significant entities from the chapter, identifying the building blocks that will be crucial for understanding the story's knowledge structure. Focus on capturing both explicit and implicit elements that carry meaning or importance in the narrative.\n\n"
        )
        if has_story_metadata:
            p += (
                "\n# Story Context\n" +
                (f"Story Title: {self.story_title}\n" if self.story_title else "") +
                (f"Genres: {', '.join(self.genres)}\n" if self.genres else "") +
                (f"Additional Tags: {', '.join(self.additional_tags)}\n" if self.additional_tags else "") +
                (f"Story Description: {self.story_description}\n" if self.story_description else "")
            )
        
        if has_story_summaries:
            p += (
                "\n# Reader Context\n" +
                (f"## Story Summary (Known to Reader)\n{self.story_summary}\n" if self.story_summary else "") +
                (f"## Summary of Recent Chapters\n{self.last_n_chapters_summary}\n" if self.last_n_chapters_summary else "")
            )
        
        if has_chapter_data:
            p += (
                "\n# Narrative Content\n" +
                (f"## Chapter Title\n{self.chapter_title}\n" if self.chapter_title else "") +
                (f"## Chapter Content\n---\n{self.chapter_content}\n---\n" if self.chapter_content else "")
            )
            
        p += (
            "\n# Purpose\n" +
            "Extract all significant entities mentioned in this chapter, focusing on elements that have narrative importance or impact on the story.\n"
        )
        
        p += (
            "\n# Guidelines\n\n" +
            "## Entity Categories\n" +
            "Extract important entities for the following categories:\n"
        )
        
        for i, entity in enumerate(EntityType):
            p += (
                f"{i+1}. {entity.value}s: {entity.description}\n"
            )
        
        p += (
            "\n## Format\n" +
            "For each entity, include the following fields:\n" +
            "- Main Identifier of the entity that will be used to reference the entity and you believe is unique\n" +
            "- Aliases (all names and other identifiers for the entity)\n" +
            "- Description of the entity (what the entity is, what it does, etc)\n" +
            "- Narrative Significance (why this entity matters in the context of this chapter)\n" +
            "- Significance Level to the chapter's plot (central - crucial to everything; major - crucial to current events; supporting - actively involved in current events; minor - relevant but not crucial; background - not important to current events; peripheral - mentioned but barely relevant)\n" +
            "- other related entities mentioned\n"
        )
        
        p += (
            "\n## Extraction Rules\n" +
            "- Extract only entities with clear narrative significance that will be important across the entire story\n" +
            "- Make sure to combine entities that reference the same entity (describe the entity in more detail if needed)\n" +
            "- Include both explicitly named and strongly implied entities\n" +
            "- Note uncertainty when entity details are ambiguous\n" +
            "- Focus on quality over quantity - only include truly significant entities\n"
        )
        
        p += (
            "\n## Important Notes\n" +
            "- Make sure only significant entities are included\n" +
            "- Note if an entity's nature or description is unclear or evolving\n" +
            ("- Please format the entities using JSON with ```json to make it easy to parse\n" if not self.is_structured_output else "")
        )
        
        if not self.is_structured_output:
            p += ("\n## Example Output" +
"""
```json
{
    "time_periods": [],
    ...
    "characters": [
        {
            "identifier": "John Doe",
            "aliases": ["John", "Doe", "JD", "Protagonist"],
            "description": "A young man with a kind heart and a strong sense of justice.",
            "narrative_significance": "John Doe is the protagonist of the story, and his journey is central to the plot.",
            "significance_level": "central",
            "related_entities": ["Jane Smith", "Bob Johnson"]
        },
        {
            "identifier": "John Doe's Dog",
            "aliases": [],
            "description": "A loyal and friendly dog who accompanies John Doe on his journey.",
            "narrative_significance": "The dog is a companion to John Doe and provides emotional support throughout the story.",
            "significance_level": "supporting",
            "related_entities": ["John Doe"]
        },
        ...
    ],
    ...
}
```
""")
        return p
    
    @classmethod
    def template(cls) -> 'FindEntitiesTemplate':
        # Return a new instance of the prompt template with placeholder values.
        return cls(
            story_title="{{story_title}}",
            genres=["{{genre1}}", "{{genre2}}", "{{genre3}}"],
            additional_tags=["{{additional_tag1}}", "{{additional_tag2}}", "{{additional_tag3}}"],
            story_description="{{story_description}}",
            chapter_title="{{chapter_title}}",
            chapter_content="{{chapter_content}}",
            story_summary="{{story_summary}}",
            last_n_chapters_summary="{{last_n_chapters_summary}}",
            is_structured_output=False,
        )


class FindEntitiesPrompt(PromptBase):
    """Prompt for reading a chapter of a book"""
    
    def __init__(
        self,
        model_config: ModelConfig | None = None,
        prompt_template: FindEntitiesTemplate | None = None,
    ) -> None:
        """Initialize the prompt"""
        if model_config is None:
            # gemini-2.0-flash-001 seems to be good for this task
            # gemini-2.0-flash-lite-preview-02-05 seems to also be good for this task
            # nice b/c they are super cheap, plus they have structured output - https://ai.google.dev/gemini-api/docs/structured-output?lang=python
            # interestingly, thinking models are NOT good for this task
            model_config = ModelConfig(
                provider=Provider.GEMINI,
                model="gemini-2.0-flash-001",
                temperature=0.8,
            )

        super().__init__(model_config, prompt_template)
    
    @property
    def name(self) -> str:
        return "Find Entities"
    
    @property
    def version(self) -> int:
        return 1
    
    @property
    def type(self) -> PromptType:
        return PromptType.FIND_ENTITIES
    
    @property
    def description(self) -> str:
        return "Extract all narratively significant entities from a chapter of a book"
