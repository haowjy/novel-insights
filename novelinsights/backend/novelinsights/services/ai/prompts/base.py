from dataclasses import dataclass
from typing import Any, Dict, Mapping
from abc import ABC, abstractmethod
from packaging.version import Version

from novelinsights.core.config import ModelConfig
from novelinsights.types.services.prompt import PromptType

@dataclass
class PromptRequest:
    prompt: str
    estimated_tokens: int
    estimated_cost: float

@dataclass
class PromptTemplateBase(ABC):
    """Base class for all prompt templates"""
    
    def update(self, **kwargs: Any) -> None:
        """Update the template with given parameters"""
        for k, v in kwargs.items():
            setattr(self, k, v)
    
    @abstractmethod
    def template(self) -> 'PromptTemplateBase':
        """Template for the prompt"""
        raise NotImplementedError("Subclasses must implement this method")
    
    @abstractmethod
    def prompt(self) -> str:
        """Prompt for the template"""
        raise NotImplementedError("Subclasses must implement this method")
    
    

class DefaultPromptTemplate(PromptTemplateBase):
    def template(self) -> 'PromptTemplateBase':
        return self

    def prompt(self) -> str:
        return ""

class PromptBase(ABC):
    """Base class for all prompts"""
    
    #
    # Base Model and Parameters Definitions
    #
    
    def __init__(
        self, 
        model_config: ModelConfig | None = None,
        prompt_template: PromptTemplateBase | None = None,
    ) -> None:
        self._model_config: ModelConfig = model_config or ModelConfig()
        self._prompt_template: PromptTemplateBase = prompt_template or DefaultPromptTemplate()
        self._last_rendered: str = ""
    
    @property
    def model_config(self) -> ModelConfig:
        """Model configuration"""
        return self._model_config
    
    @property
    def prompt_template(self) -> PromptTemplateBase:
        """Prompt template"""
        return self._prompt_template
    
    @property
    def last_rendered(self) -> str:
        """Last rendered prompt"""
        return self._last_rendered
    
    #
    # Abstract methods
    #
    @abstractmethod
    def _prompt(self) -> str:
        """Prompt template"""
        raise NotImplementedError("Subclasses must implement this method")
    
    @abstractmethod
    def render(self, **kwargs: Any) -> PromptRequest:
        """Render the template with given parameters into a prompt and return it as a string"""
        raise NotImplementedError("Subclasses must implement this method")
    
    @abstractmethod
    def render_example(self) -> PromptRequest:
        """Render the template with ALL placeholder values. Does not update the last rendered prompt."""
        raise NotImplementedError("Subclasses must implement this method")
    
    #
    # Abstract properties
    #
    
    @property
    @abstractmethod
    def version(self) -> Version:
        """Version of the prompt"""
        return Version("0.0.1")
    
    @property
    @abstractmethod
    def type(self) -> PromptType:
        """Type of the prompt"""
        return PromptType.BASE
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Unique identifier for the prompt"""
        return "__base__"
    
    @property
    @abstractmethod
    def description(self) -> str:
        """Description of the prompt"""
        return "DO NOT USE THIS PROMPT DIRECTLY. Use it as a base for other prompts."
