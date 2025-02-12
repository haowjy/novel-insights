from dataclasses import dataclass
from typing import Any
from abc import ABC, abstractmethod
from packaging.version import Version

from novelinsights.core.config import ModelConfig
from novelinsights.types.services.prompt import PromptType
from novelinsights.utils.token import TokenEstimator

@dataclass
class PromptRequest:
    prompt: str
    estimated_tokens: int

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
        prompt_template: PromptTemplateBase,
        model_config: ModelConfig | None = None,
    ) -> None:
        self._prompt_template: PromptTemplateBase = prompt_template
        self._model_config: ModelConfig = model_config or ModelConfig()
        self._last_rendered: str = ""
    
    @property
    def model_config(self) -> ModelConfig:
        """Model configuration"""
        return self._model_config
    
    @property
    def prompt_template(self) -> PromptTemplateBase:
        """Prompt template"""
        return self._prompt_template
    
    def update_prompt_template(self, **kwargs: Any) -> None:
        """Update the prompt template"""
        self._prompt_template.update(**kwargs)
    
    @property
    def last_rendered(self) -> str:
        """Last rendered prompt"""
        return self._last_rendered
    
    def _prompt(self, **kwargs: Any) -> str:
        """Prompt template"""
        return self._prompt_template.prompt(**kwargs)
    
    def render(self, **kwargs: Any) -> PromptRequest:
        """Render the prompt with given parameters"""
        # update prompt config with kwargs
        p = self._prompt(**kwargs)
        pr = PromptRequest(
            prompt=p,
            estimated_tokens=TokenEstimator.simple(p),
        )
        return pr
    
    def render_example(self) -> PromptRequest:
        """Render an example prompt with all placeholder values"""
        p = self._prompt_template.template().prompt()
        pr = PromptRequest(
            prompt=p,
            estimated_tokens=TokenEstimator.simple(p),
        )
        
        return pr
    
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
