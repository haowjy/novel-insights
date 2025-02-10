from typing import Any, Optional
from dataclasses import dataclass

from sympy import Equality

from novelinsights.services.ai.prompts.narrative.mixins import NarrativeExtractionMixin
from novelinsights.services.ai.prompts.base import PromptTemplateBase
from novelinsights.types.knowledge import NodeType

@dataclass
class FindEntitiesTemplate(NarrativeExtractionMixin, PromptTemplateBase):
    # Chapter data
    chapter_title: str # Can just be the chapter number
    chapter_content: str # REQUIRED: preferred format: markdown
    
    # Summaries of the story so far
    story_summary: Optional[str] = None # summary of the entire story so far
    last_n_chapters_summary: Optional[str] = None # concatenate the summaries of the last n chapters
    
    # Summaries of related entities
    # related_entities: Optional[list[str]] = None
    
    def has_chapter_data(self) -> bool:
        return bool(self.chapter_title and self.chapter_content)
    
    def has_story_summaries(self) -> bool:
        return bool(self.story_summary or self.last_n_chapters_summary)
    
    # def has_related_entities(self) -> bool:
    #     return bool(self.related_entities)
    
    def prompt(self, **kwargs: Any) -> str:
        # update prompt config with kwargs
        self.update(**kwargs)
        
        has_story_metadata = self.has_story_metadata()
        has_chapter_data = self.has_chapter_data()
        has_story_summaries = self.has_story_summaries()
        # has_related_entities = self.has_related_entities()
        
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
        
        # if has_related_entities:
        #     p += (
        #         "\n# Related Entities\n" +
        #         (f"{'\n'.join(self.related_entities)}\n" if self.related_entities else "")
        #     )
        
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
            "Extract entities in the following categories:\n"
        )
        
        for i, node in enumerate(NodeType):
            p += (
                f"{i+1}. {node.name}: {node.description}\n"
            )

        p += (
            "\n## For Each Entity Include\n" +
            "1. Category (from above)\n" +
            "2. Name/Identifier\n" +
            "3. Brief Description\n" +
            "4. Narrative Significance (Why this entity matters in the context of this chapter)\n" +
            "5. Cross-references (other entities mentioned in the same chapter that are related to this entity)\n" + 
            "6. Significance Level to the chapter's plot (critical, major, minor, supporting, background, incidental)\n" +
            "7. Do not include background or incidental entities\n" +
            "8. Do not include entities that are only mentioned in passing or are not central to the plot of this chapter\n"
        )
        
        p += (
            "\n## Extraction Rules\n" +
            "- Extract only entities with clear narrative significance\n" +
            "- Entities that are the same should be the same entity\n" +
            "- Include both explicitly named and strongly implied entities\n" +
            "- Note uncertainty when entity details are ambiguous\n" +
            "- Focus on quality over quantity - only include truly significant entities\n" +
            "- Maintain chapter-specific focus (only what's mentioned/relevant in this chapter)\n"
        )
        
        p += (
            "\n## Important Notes\n" +
            "- Sort entities by category, then by order of appearance\n" +
            "- Include cross-references between related entities\n" +
            "- Note if an entity's nature or description is unclear or evolving\n" +
            "- Maintain focus on this chapter's content only\n" +
            "- Please format the entities using Markdown to provide a clear and readable list\n" +
            f"- Start with '# Entity Extraction' and don't include any else other than the list of entities\n"
        )

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
            # related_entities=["{{related_entity1}}", "{{related_entity2}}", "{{related_entity3}}"],
        )
