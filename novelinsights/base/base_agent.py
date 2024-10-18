
from abc import abstractmethod
from novelinsights.utils import get_estimator,LLMWrapper
from typing import List
from pydantic import BaseModel
from qdrant_client import QdrantClient
import logging

class AgentHistory(BaseModel):
    prompt: str
    response: str

class BaseAgent():
    @abstractmethod
    def __init__(self, llm: LLMWrapper, db: QdrantClient):
        """Base class for an agent that interacts with an LLM model.
        
        Args:
            llm (LLMWrapper): The LLM model wrapper to interact with.
            response_model (BaseModel): The response model for the generated responses.
        """
        self.agent_history:List[AgentHistory] = []
        
        self.llm = llm
        self.db = db
        
    @abstractmethod
    def get_prompt(self) -> str:
        raise NotImplementedError("prompt method must be implemented in derived class")
    
    @abstractmethod
    def get_response_fields(self) -> dict:
        return NotImplementedError("response_fields method must be implemented in derived class")
    
    @abstractmethod
    def generate(self, prompt: str) -> str:
        resp_str = self.llm.generate(prompt)
        logging.debug(f"prompt tokens: {self.llm.estimate_tokens(prompt)}")
        logging.debug(f"response tokens: {self.llm.estimate_tokens(resp_str)}")
        self.agent_history.append(AgentHistory(prompt=prompt, response=resp_str))
        return resp_str
    
    @abstractmethod
    def _mock_generate(self, prompt: str, response: str) -> str:
        """Mock the generate method for testing purposes."""
        logging.debug(f"prompt tokens: {self.llm.estimate_tokens(prompt)}")
        logging.debug(f"response tokens: {self.llm.estimate_tokens(response)}")
        self.agent_history.append(AgentHistory(prompt=prompt, response=response))
        return response
    
    @abstractmethod
    def estimate_tokens(self, prompt: str) -> int:
        if self.llm is None:
            return get_estimator()(prompt) 
        return self.llm.estimate_tokens(prompt)
    
    def __repr__(self) -> str:
        return self.llm.__repr__()
    
    def __str__(self) -> str:
        return self.llm.__str__()