from novelinsights.types.base import DescribedEnum

from typing import Type

class PromptType(DescribedEnum):
    BASE = ("base", "Base prompt type")
    SUMMARIZE_CHAPTER = ("summarize_chapter", "Summarize a chapter of a book")
    EXTRACT_CHAPTER_KNOWLEDGE = ("extract_chapter_knowledge", "Extract knowledge from a chapter of a book")
    # CHAPTER_READER = "chapter_reader"
    # ARTICLE_CREATION = "article_creation"
    # NODE_CREATION = "node_creation"
    # NODE_STATE_CREATION = "node_state_creation"
    
    def get_prompt_class(self) -> Type:
        """Get the prompt class for this type"""
        from novelinsights.services.ai.prompts.narrative.chapterbychapter.summarize import SummarizeChapterPrompt
        from novelinsights.services.ai.prompts.narrative.chapterbychapter.extract import ExtractChapterKnowledgePrompt
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
            PromptType.SUMMARIZE_CHAPTER: SummarizeChapterPrompt,
            PromptType.EXTRACT_CHAPTER_KNOWLEDGE: ExtractChapterKnowledgePrompt,
        }
        return prompt_map[self]
