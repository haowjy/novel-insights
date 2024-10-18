from typing import Literal, Union, List

from llama_index.core.llms import ChatMessage
from llama_index.core.llms.llm import LLM
from llama_index.core.utils import Tokenizer

from novelinsights.utils import get_estimator

class LLMWrapper:
    """Wrapper around the LLM class from llama_index."""
    def __init__(self, llm:LLM, mode: Literal["completion", "chat"] = "completion", tokenizer:Tokenizer | str = None, system_prompt: str = None):
        self.llm = llm
        self.mode = mode
        self.system_prompt = system_prompt
        self.estimator = get_estimator(tokenizer)
    
    def chat(self, messages: List[ChatMessage]) -> str:
        """Chat with the LLM model."""
        return self.llm.chat(messages)
    
    def complete(self, prompt: str) -> str:
        """Complete a prompt with the LLM model."""
        return self.llm.complete(prompt)
        
    def generate(self, prompt: Union[str, List[ChatMessage]], system_prompt: str="") -> str:
        """Generate a response from the LLM model given a chat message."""
        this_system_prompt = system_prompt if system_prompt else self.system_prompt
        
        if self.mode == "chat":
            if isinstance(prompt, str):
                messages = []
                if this_system_prompt:
                    messages.append(ChatMessage(role="system", content=this_system_prompt))
                messages.append(ChatMessage(role="user", content=prompt))
            else:
                messages = prompt
            response = self.chat(messages)
            response = response.message.content
            
        elif self.mode == "completion":
            response = self.complete(prompt)
            response = response.content
        
        return response
    
    def estimate_tokens(self, prompt: str) -> int:
        """Estimate the number of tokens in the response given a prompt."""
        return self.estimator(prompt)
    
    def max_tokens(self) -> int:
        """Get the maximum number of tokens the model can handle."""
        return self.llm
        
    def set_system_prompt(self, system_prompt: str):
        """Set the system prompt for the model."""
        self.system_prompt = system_prompt
    
    def set_mode(self, mode: Literal["chat", "completion"]):
        """Set the mode of the model."""
        self.mode = mode
        
    def __repr__(self) -> str:
        return self.llm.__repr__()