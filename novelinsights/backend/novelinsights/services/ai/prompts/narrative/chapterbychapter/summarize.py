from dataclasses import dataclass
from typing import Any, Optional, NotRequired
from packaging.version import Version

from novelinsights.core.config import ModelConfig
from novelinsights.services.ai.prompts.narrative.mixins import NarrativeExtractionMixin
from novelinsights.services.ai.prompts.base import PromptBase, PromptRequest, PromptTemplateBase
from novelinsights.types import (
    Provider,
    PromptType,
)

@dataclass
class SummarizeChapterTemplate(NarrativeExtractionMixin, PromptTemplateBase):
    # Chapter data
    chapter_title: str # Can just be the chapter number
    chapter_content: str # REQUIRED: preferred format: markdown
    
    # Summaries of the story so far
    story_summary: Optional[str] = None # summary of the entire story so far
    last_n_chapters_summary: Optional[str] = None # concatenate the summaries of the last n chapters
    
    # Summaries of related entities
    related_entities: Optional[list[str]] = None
    
    def has_chapter_data(self) -> bool:
        return bool(self.chapter_title and self.chapter_content)
    
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
            "- Generate a comprehensive but concise summary that captures key narrative developments, character progressions, and plot elements (including potential foreshadowing) from the provided story excerpt.\n"
            "- Maintain clarity and conciseness\n"
            "- The summary should reflect only information available to the reader at this point in the story.\n"
            "- Let's try to be precise about this summary: only include the important stuff. Stuff that can be inferred doesn't have to be included.\n"
            "- Separate the summary scene by scene\n"
            "- Please format the summary using Markdown to provide a clear and readable summary.\n"
            f"- Start the summary with '# Summary of {self.chapter_title}'\n"
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
        )

class SummarizeChapterPrompt(PromptBase):
    """Prompt for reading a chapter of a book"""
    
    def __init__(
        self,
        model_config: ModelConfig | None = None,
        prompt_config: SummarizeChapterTemplate | None = None,
    ) -> None:
        """Initialize the prompt"""
        if model_config is None:
            model_config = ModelConfig(
                provider=Provider.ANTHROPIC,
                model="claude-3-5-sonnet-20240620",
                temperature=1.0,
            )

        super().__init__(model_config, prompt_config)
        self._prompt_config: SummarizeChapterTemplate
    
    
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
    
    
    def _prompt(self, **kwargs: Any) -> str:
        return self.prompt_template.prompt(**kwargs)
    
    def render(self, **kwargs: Any) -> PromptRequest:
        # update prompt config with kwargs
        
        pr = PromptRequest(
            prompt=self.prompt_template.prompt(**kwargs),
            estimated_tokens=0,
            estimated_cost=0,
        )
        
        # render the prompt
        return pr
    
    def render_example(self) -> PromptRequest:
        return PromptRequest(
            prompt=SummarizeChapterTemplate.template().prompt(),
            estimated_tokens=0,
            estimated_cost=0,
        )
    
    
