from dataclasses import dataclass
from typing import Dict, Any
from abc import ABC, abstractmethod
from packaging.version import Version

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
        model: str = "claude-3-5-sonnet-20241022",
        model_params: None | Dict[str, Any] = None,
        prompt_params: None | Dict[str, Any] = None
        ):
        self._model: str = model
        self._model_params: Dict[str, Any] = model_params or {"max_tokens": 1000}
        self._prompt_params: Dict[str, Any] = prompt_params or {}
        self._last_rendered: str = ""

    @property
    def model(self) -> str:
        """The model to use for the prompt"""
        return self._model
    
    @property
    def model_params(self, **kwargs: Any) -> Dict[str, Any]:
        """Get or set model parameters"""
        if kwargs:
            self._model_params.update(kwargs)
            
        return self._model_params
    
    @property
    @abstractmethod
    def prompt_params(self, **kwargs: Any) -> Dict[str, Any]:
        """Get or set prompt parameters"""
        if kwargs:
            self._prompt_params.update(kwargs)
        
        return self._prompt_params

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
