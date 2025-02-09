from novelinsights.types.base import DescribedEnum

from typing import Type

class PromptType(DescribedEnum):
    BASE = ("base", "Base prompt type")
    READ_CHAPTER = ("read_chapter", "Read a chapter of a book")
    # CHAPTER_READER = "chapter_reader"
    # ARTICLE_CREATION = "article_creation"
    # NODE_CREATION = "node_creation"
    # NODE_STATE_CREATION = "node_state_creation"
    
    def get_prompt_class(self) -> Type:
        """Get the prompt class for this type"""
        from novelinsights.services.ai.prompts.narrative.read_chapter import ReadChapterPrompt
        # from .article_creation import ArticleCreationPrompt
        # from .node_creation import NodeCreationPrompt
        # from .node_state_creation import NodeStateCreationPrompt
        
        # prompt_map = {
        #     PromptType.CHAPTER_READER: ChapterReaderPrompt,
        #     PromptType.ARTICLE_CREATION: ArticleCreationPrompt,
        #     PromptType.NODE_CREATION: NodeCreationPrompt,
        #     PromptType.NODE_STATE_CREATION: NodeStateCreationPrompt,
        # }
        prompt_map = {
            PromptType.READ_CHAPTER: ReadChapterPrompt,
        }
        return prompt_map[self]
