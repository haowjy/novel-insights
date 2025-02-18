from dataclasses import asdict, dataclass, replace
from typing import Any, Optional
from packaging.version import Version

from novelinsights.core.config import ModelConfig
from novelinsights.services.ai.prompts.narrative.mixins import NarrativeChapterMixin, NarrativeStoryMixin
from novelinsights.services.ai.prompts.base import PromptBase, PromptTemplateBase
from novelinsights.types import (
    Provider,
    PromptType,
)

@dataclass
class SummarizeChapterTemplate(PromptTemplateBase, NarrativeStoryMixin, NarrativeChapterMixin):
    
    # Summaries of the story so far
    story_summary: Optional[str] = None # summary of the entire story so far
    last_n_chapters_summary: Optional[str] = None # concatenate the summaries of the last n chapters
    
    # Summaries of related entities
    related_entities: Optional[list[str]] = None
    
    def has_story_summaries(self) -> bool:
        return bool(self.story_summary or self.last_n_chapters_summary)
    
    def has_related_entities(self) -> bool:
        return bool(self.related_entities)
    
    def prompt(self, **kwargs: Any) -> str:
        # update prompt config with kwargs
        self.update(**kwargs)
        
        has_story_metadata = self.has_story_metadata()
        has_chapter_data = self.has_chapter_data()
        has_story_summaries = self.has_story_summaries()
        has_related_entities = self.has_related_entities()
        
        p = (
            f"{self._persona()}\n\n"
            f"{self._overarching_goal()}\n"
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
        
        if has_related_entities:
            p += (
                "\n# Related Entities\n" +
                (f"{'\n'.join(self.related_entities)}\n" if self.related_entities else "")
            )
        
        if has_chapter_data:
            p += (
                "\n# Narrative Content\n" +
                (f"## Chapter Title\n{self.chapter_title}\n" if self.chapter_title else "") +
                (f"## Chapter Content\n---\n{self.chapter_content}\n---\n" if self.chapter_content else "")
            )
        
        p += (
            "\n# Instructions\n"
            "- Generate a comprehensive summary that captures key narrative/plot developments, and major literary elements (e.g. foreshadowing, symbolism, allusions, etc.) from the provided chapter woven into the summary\n"
            "- The summary should reflect only information available to the reader at this point in the story, or information that is common knowledge of through literary allusions/pop culture references\n"
            "- Separate the summary scene by scene and weave in literary elements\n"
            "- Please format the summary using Markdown to provide a clear and readable summary\n"
            f"- Start the summary with '<|STARTOFSUMMARY|># Summary of {self.chapter_title}' and end with '<|ENDOFSUMMARY|>'"
        )
        
        return p
    
    @classmethod
    def template(cls) -> 'SummarizeChapterTemplate':
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
            related_entities=["{{related_entity1}}", "{{related_entity2}}", "{{related_entity3}}"],
            structured_output_schema=None,
        )

class SummarizeChapterPrompt(PromptBase):
    """Prompt for reading a chapter of a book"""
    
    def __init__(
        self,
        model_config: ModelConfig | None = None,
        prompt_template: SummarizeChapterTemplate | None = None,
    ) -> None:
        """Initialize the prompt"""
        
        # deepseek r1 distill llama 70B should be good enough
        # deepseek r1 seems to be the best
        # o1-mini seems to be good as well, not the best, I think thinking models will be best for this task
        # Claude 3.5 Sonnet is good for just a summary of the events of the chapter, but maybe with some extra prompting, the literary elements can also be extracted well
        cur_model_config = ModelConfig(
                provider=Provider.ANTHROPIC,
                model="claude-3-5-sonnet-20241022",
                temperature=0.8,
                max_tokens=8192,
            )
        
        if model_config is not None:
            cur_model_config = replace(cur_model_config, **asdict(model_config))
            
        super().__init__(
            prompt_template or SummarizeChapterTemplate.template(),
            cur_model_config,
        )
    
    @property
    def name(self) -> str:
        return "Summarize Chapter"
    
    @property
    def version(self) -> Version:
        return Version("0.0.1")
    
    @property
    def type(self) -> PromptType:
        return PromptType.SUMMARIZE_CHAPTER
    
    @property
    def description(self) -> str:
        return "Summarize a chapter of a book"
