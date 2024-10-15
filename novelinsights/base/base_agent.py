
from novelinsights.base.base_llm import LLMWrapper
from novelinsights.utils import get_estimator
from typing import List
from pydantic import BaseModel
from qdrant_client import QdrantClient

class AgentHistory(BaseModel):
    prompt: str
    response: str

class BaseAgent():
    def __init__(self, llm: LLMWrapper):
        """Base class for an agent that interacts with an LLM model.
        
        Args:
            llm (LLMWrapper): The LLM model wrapper to interact with.
            response_model (BaseModel): The response model for the generated responses.
        """
        self.agent_history:List[AgentHistory] = []
        
        self.llm = llm
        
    def prompt(self) -> str:
        raise NotImplementedError("prompt method must be implemented in derived class")
    
    def generate(self, prompt: str) -> str:
        resp_str = self.llm.generate(prompt)
        self.agent_history.append(AgentHistory(prompt=prompt, response=resp_str))
        return resp_str
    
    def _mock_generate(self, prompt: str, response: str) -> str:
        """Mock the generate method for testing purposes."""
        self.agent_history.append(AgentHistory(prompt=prompt, response=response))
        return response
    
    def estimate_response_tokens(self, prompt: str) -> int:
        if self.llm is None:
            return get_estimator()(prompt) 
        return self.llm.estimate_response_tokens(prompt)
    
    def __repr__(self) -> str:
        return self.llm.__repr__()
    
    def __str__(self) -> str:
        return self.llm.__str__()