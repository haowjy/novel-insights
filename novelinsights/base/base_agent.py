
from novelinsights.base.base_llm import LLMWrapper
from novelinsights.utils import get_estimator

class BaseAgent():
    def __init__(self, llm: LLMWrapper):
        self.llm = llm
        
    def prompt(self) -> str:
        raise NotImplementedError("prompt method must be implemented in derived class")
    
    def generate_response(self) -> str:
        raise NotImplementedError("generate_response method must be implemented in derived class")
    
    def estimate_response_tokens(self, prompt: str) -> int:
        if self.llm is None:
            return get_estimator()(prompt) 
        return self.llm.estimate_response_tokens(prompt)
    
    def __repr__(self) -> str:
        return self.llm.__repr__()
    
    def __str__(self) -> str:
        return self.llm.__str__()