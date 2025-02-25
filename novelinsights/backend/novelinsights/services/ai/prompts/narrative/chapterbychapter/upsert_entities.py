from typing import Any, Optional
from dataclasses import asdict, dataclass, replace

from novelinsights.core.config import ModelConfig
from novelinsights.schemas.prompt_responses.narrative.chapterbychapter.upsert_entities import UpsertEntitiesOutputSchema
from novelinsights.services.ai.prompts.narrative.mixins import NarrativeChapterMixin, NarrativeStoryMixin
from novelinsights.services.ai.prompts.base import PromptBase, PromptTemplateBase
from novelinsights.types.services.prompt import PromptType
from novelinsights.types.services.provider import Provider

@dataclass
class UpsertEntitiesTemplate(PromptTemplateBase, NarrativeStoryMixin, NarrativeChapterMixin):
    
    # Entities to create or update with
    new_entities: list[str]
    
    # Summaries of the story so far
    story_summary: Optional[str] = None # summary of the entire story so far
    last_n_chapters_summary: Optional[str] = None # concatenate the summaries of the last n chapters
    
    # Summaries of existing entities to update
    existing_entities: Optional[list[str]] = None
    
    def has_story_summaries(self) -> bool:
        return bool(self.story_summary or self.last_n_chapters_summary)
    
    def has_existing_entities(self) -> bool:
        return bool(self.existing_entities)

    def prompt(self, **kwargs: Any) -> str:
        # update prompt config with kwargs
        self.update(**kwargs)
        
        has_story_metadata = self.has_story_metadata()
        has_chapter_data = self.has_chapter_data()
        has_story_summaries = self.has_story_summaries()
        has_existing_entities = self.has_existing_entities()
        
        p = (
            f"{self._persona()}\n\n" +
            "# Overarching Goal\n" +
            "Update or create the entities in the chapter, focusing on elements that have narrative importance or impact on the story\n"
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
            
        if has_existing_entities:
            p += (
                "\n# Existing Entities\n" +
                (f"{'\n'.join(self.existing_entities)}\n" if self.existing_entities else "")
            )
        
        p += (
            "\n# Purpose\n" +
            "Update or create the entities in the chapter, as well as the relationships between them.\n"
        )
        
        p += (
            "\n# Guidelines\n\n" +
            "## Entities\n" +
            "Update or create the entities for the following entities:\n"
        )
        
        p += (
            "### Extracted Entites to Create or Update\n"
        )
        for entity in self.new_entities:
            p += (
                f"{entity}\n"
            )
        
        p += (
            "\n## Rules\n" +
            "- Make sure to combine entities that reference the same entity (describe the entity in more detail and update the identifier if needed)\n" +
            "- Note uncertainty when entity details are ambiguous\n" +
            ("- Please format the entities using JSON with ```json to make it easy to parse\n" if not self.has_structured_out else "")
        )
        
        if not self.has_structured_out:
            p += (
                "\n## Output JSON Schema" +
                f"{UpsertEntitiesOutputSchema.model_json_schema()}"
                )
        
        return p
    
    @classmethod
    def template(cls) -> 'UpsertEntitiesTemplate':
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
            
            new_entities=["{{new_entity1}}", "{{new_entity2}}", "{{new_entity3}}"],
            existing_entities=["{{existing_entity1}}", "{{existing_entity2}}", "{{existing_entity3}}"],
            
            structured_output_schema=None,
        )


class UpsertEntitiesPrompt(PromptBase):
    """Prompt for updating or creating the entities that appear in a chapter of a book"""
    
    def __init__(
        self,
        model_config: ModelConfig | None = None,
        prompt_template: UpsertEntitiesTemplate | None = None,
    ) -> None:
        """Initialize the prompt"""
        # gemini-2.0-flash-001 seems to be good for this task
        # gemini-2.0-flash-lite-preview-02-05 seems to also be good for this task
        # nice b/c they are super cheap, plus they have structured output - https://ai.google.dev/gemini-api/docs/structured-output?lang=python
        # interestingly, thinking models are NOT good for this task
        cur_model_config = ModelConfig(
            provider=Provider.GOOGLE,
            max_tokens=8192, # maybe 4096 can be enough?
            model="gemini-2.0-flash-001",
            temperature=0.8,
        )
        
        if model_config is not None:
            cur_model_config = replace(cur_model_config, **asdict(model_config))
            
        super().__init__(
            prompt_template or UpsertEntitiesTemplate.template(),
            cur_model_config,
        )
    
    @property
    def name(self) -> str:
        return "Upsert Entities"
    
    @property
    def version(self) -> int:
        return 1
    
    @property
    def type(self) -> PromptType:
        return PromptType.UPSERT_ENTITIES
    
    @property
    def description(self) -> str:
        return "Update or create the entities in a chapter of a book"
