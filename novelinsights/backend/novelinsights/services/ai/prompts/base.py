from dataclasses import dataclass
from typing import Any, Dict, TypedDict
from abc import ABC, abstractmethod
from packaging.version import Version

from novelinsights.core.config import ModelConfig
from novelinsights.types.services.prompt import PromptType

@dataclass
class PromptRequest:
    prompt: str
    estimated_tokens: int
    estimated_cost: float

class PromptBase(ABC):
    """Base class for all prompt templates"""
    
    #
    # Base Model and Parameters Definitions
    #
    
    def __init__(
        self, 
        model_config: ModelConfig | None = None,
        prompt_config: Dict[str, Any] | None = None,
    ) -> None:
        self._model_config: ModelConfig = model_config or ModelConfig()
        self._prompt_config: Dict[str, Any] = prompt_config or {}
        self._last_rendered: str = ""
    
    @property
    def model_config(self) -> ModelConfig:
        """Model configuration"""
        return self._model_config
    
    @property
    @abstractmethod
    def prompt_config(self) -> Dict[str, Any]:
        """Prompt configuration"""
        raise NotImplementedError("Subclasses must implement this method")
    
    @property
    def last_rendered(self) -> str:
        """Last rendered prompt"""
        return self._last_rendered
    
    #
    # Abstract methods
    #
    
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
