from typing import Dict, Any
from abc import ABC, abstractmethod

class PromptTemplate(ABC):
    @abstractmethod
    def render(self, **kwargs: Any) -> str:
        """Render the prompt with given parameters"""
        pass
    
    @property
    def version(self) -> str:
        return "1.0"