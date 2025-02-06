from dataclasses import dataclass
from typing import Dict, Any
from abc import ABC, abstractmethod
from packaging.version import Version

from novelinsights.services.ai.prompts.types import PromptType

@dataclass
class PromptResult:
    prompt: str
    tokens_used: int
    estimated_cost: float

class PromptTemplate(ABC):
    """Base class for all prompt templates"""
    
    def __init__(self):
        self._model: str = "claude-3-5-sonnet-20241022"
        self._parameters: Dict[str, Any] = {"max_tokens": 1000}
    
    def set_model(self, model: str) -> "PromptTemplate":
        """Set the model to use for the prompt"""
        self._model = model
        return self
    
    def set_parameter(self, key: str, value: Any) -> "PromptTemplate":
        """Set a single parameter"""
        self._parameters[key] = value
        return self

    def set_parameters(self, parameters: Dict[str, Any] | None = None, **kwargs: Any) -> "PromptTemplate":
        """Set multiple parameters via dict or kwargs"""
        if parameters:
            self._parameters.update(parameters)
        self._parameters.update(kwargs)
        return self
    
    @property
    def model(self) -> str:
        """The model to use for the prompt"""
        return self._model
    
    @property
    def parameters(self) -> Dict[str, Any]:
        """Parameters of the prompt"""
        return self._parameters

    
    #
    # Abstract methods
    #
    
    @abstractmethod
    def render(self, **kwargs: Any) -> PromptResult:
        """Render the template with given parameters into a prompt and return it as a string"""
        pass
    
    @abstractmethod
    def render_example(self) -> PromptResult:
        """Render the template with ALL placeholder values. Does not update the last rendered prompt."""
        pass
    
    #
    # Abstract properties
    #
    
    @property
    @abstractmethod
    def last_rendered(self) -> str:
        """Last rendered prompt"""
        pass
    
    @property
    @abstractmethod
    def version(self) -> Version:
        """Version of the prompt"""
        pass 
    
    @property
    @abstractmethod
    def type(self) -> PromptType:
        """Type of the prompt"""
        pass
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Unique identifier for the prompt"""
        pass
    
    @property
    @abstractmethod
    def description(self) -> str:
        """Description of the prompt"""
        pass