from dataclasses import dataclass
from typing import Any, Optional, Type
from abc import ABC, abstractmethod
from packaging.version import Version
from pydantic import BaseModel

from novelinsights.core.config import ModelConfig
from novelinsights.services.ai.llmclient import LLMClient, LLMResponse
from novelinsights.types.services.prompt import PromptType

from novelinsights.utils.parser import extract_blocks

@dataclass
class PromptTemplateBase(ABC):
    """Base class for all prompt templates"""
    
    structured_output_schema: Optional[Type[BaseModel]]
    
    @property
    def has_structured_out(self) -> bool:
        return bool(self.structured_output_schema)
    
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
    
    def render(self, **kwargs: Any) -> str:
        """Render the prompt with given parameters"""
        # update prompt config with kwargs
        p = self._prompt(**kwargs)
        self._last_rendered = p
        return p
    
    def render_example(self) -> str:
        """Render an example prompt with all placeholder values"""
        p = self._prompt_template.template().prompt()
        return p
    
    def generate(self, client: LLMClient, store_config: bool = False, **kwargs: Any) -> LLMResponse:
        """Generate a simple text response from the LLM using the given client"""
        return client.generate(self.model_config, self.render(**kwargs), store_config=store_config)
    
    def generate_structured(self, client: LLMClient, store_config: bool = False, **kwargs: Any) -> LLMResponse:
        """Generate a structured response from the LLM using the given client"""
        if self.prompt_template.has_structured_out:
            return client.generate_structured(self.model_config, self.render(**kwargs), structured_schema=self.prompt_template.structured_output_schema, store_config=store_config)
        else:
            raise ValueError("No structured output schema defined for this prompt")

    
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
    
    def __repr__(self) -> str:
        """Representation of the prompt"""
        return f"{self.__class__.__name__}(name={self.name}, version={self.version}, type={self.type}, has_structured_out={self.prompt_template.has_structured_out}, description={self.description})"