from enum import Enum
from typing import Type
    
class PromptType(Enum):
    TEMPLATE = "template"
    # CHAPTER_READER = "chapter_reader"
    # ARTICLE_CREATION = "article_creation"
    # NODE_CREATION = "node_creation"
    # NODE_STATE_CREATION = "node_state_creation"
    
    def get_prompt_class(self) -> Type:
        """Get the prompt class for this type"""
        # from .chapter_reader import ChapterReaderPrompt
        # from .article_creation import ArticleCreationPrompt
        # from .node_creation import NodeCreationPrompt
        # from .node_state_creation import NodeStateCreationPrompt
        
        # prompt_map = {
        #     PromptType.CHAPTER_READER: ChapterReaderPrompt,
        #     PromptType.ARTICLE_CREATION: ArticleCreationPrompt,
        #     PromptType.NODE_CREATION: NodeCreationPrompt,
        #     PromptType.NODE_STATE_CREATION: NodeStateCreationPrompt,
        # }
        # return prompt_map[self]
        # TODO: Implement this
        raise NotImplementedError(f"TODO: Implement Prompt class for {self}")