from abc import ABC, abstractmethod
from dataclasses import asdict, dataclass
import json
from typing import Any, Generic, List, Literal, Optional, Type, TypeVar

from pydantic import BaseModel

from anthropic.types.message_param import MessageParam
import anthropic

from google import genai
from google.genai import types as google_types

from novelinsights.core.config import ModelConfig

@dataclass(frozen=True)
class Message:
    content: str
    role: Literal["user", "assistant"]
    
@dataclass(frozen=True)
class UsageMetadata:
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int

T = TypeVar("T", bound=BaseModel)

@dataclass
class LLMResponse(Generic[T]):
    resp: Any | T
    usage: UsageMetadata
    model_config: Optional[ModelConfig] = None
    
    def to_dict(self) -> dict:
        result = asdict(self)
        result["resp"] = self.resp.model_dump(mode="json") if isinstance(self.resp, BaseModel) else self.resp
        return result

    def to_json_str(self, indent: int = 2) -> str:
        return json.dumps(self.to_dict(), indent=indent)
    
    @classmethod
    def from_dict(cls, data: dict, resp_schema: Optional[Type[BaseModel]] = None) -> 'LLMResponse':
        # Create the instance with raw data
        instance = cls(**data)
        
        # Apply schema validation if provided
        if resp_schema and instance.resp:
            instance.resp = resp_schema.model_validate(instance.resp)
        
        return instance
    
    @classmethod
    def from_json(cls, json_str: str, resp_schema: Optional[Type[BaseModel]] = None) -> 'LLMResponse':
        data = json.loads(json_str)
        return cls.from_dict(data, resp_schema)
    

class LLMClient(ABC):
    """Abstract base class for LLM clients"""
    
    def __init__(self, client: Any):
        self.client = client

    @abstractmethod
    def generate(
        self, 
        model_config: ModelConfig,
        contents: List[Message] | str, 
        system: Optional[str] = None, 
        structured_schema: Optional[Type[BaseModel]] = None,
        store_config: bool = False,
        **kwargs: Any) -> LLMResponse:
        """Generate a prompt"""
        raise NotImplementedError("Subclasses must implement this method")
    
    @abstractmethod
    def generate_structured(
        self, 
        model_config: ModelConfig,
        contents: List[Message] | str, 
        system: Optional[str] = None, 
        structured_schema: Optional[Type[BaseModel]] = None,
        store_config: bool = False,
        **kwargs: Any) -> LLMResponse:
        """Generate a structured prompt"""
        raise NotImplementedError("Subclasses must implement this method")
    
    @abstractmethod
    def generate_chat(
        self, 
        model_config: ModelConfig,
        messages: List[Message],
        system: Optional[str] = None,
        structured_schema: Optional[Type[BaseModel]] = None,
        store_config: bool = False,
        **kwargs: Any) -> Any:
        """Generate a chat prompt"""
        raise NotImplementedError("Subclasses must implement this method")



class GoogleGeminiClient(LLMClient):
    """Google Gemini client
            
    TODO: Google supports function calling - https://ai.google.dev/gemini-api/docs/function-calling/tutorial?lang=python
    TODO: and grounding with google search - https://ai.google.dev/gemini-api/docs/grounding?lang=python
    TODO: token streaming - https://ai.google.dev/gemini-api/docs/text-generation?lang=python
    TODO: Chat
    
    """
    
    def __init__(self, client: genai.Client):
        super().__init__(client)
        self.client: genai.Client

    def __generate(
        self, 
        model_config: ModelConfig,
        contents: List[Message] | str, 
        system: Optional[str] = None, 
        structured_schema: Optional[Type[BaseModel]] = None,
        ) -> google_types.GenerateContentResponse:
        """Send LLM API request to Google Gemini
        
        Args:
            contents: List[Message] | str
            system: Optional[str]
            model_config: Optional[ModelConfig]
            structured_schema: Optional[Type[BaseModel]]
            
        Returns:
            str | None
        """
                 
        if isinstance(contents, str):
            google_contents = [Message(role="user", content=contents)]
        else:
            google_contents = contents
        
        if structured_schema:
            response_mime_type = "application/json"
            response_schema = structured_schema
        else:
            response_mime_type = None
            response_schema = None

        response = self.client.models.generate_content(
            model=model_config.model,
            contents=[m.content for m in google_contents],
            config={
            "system_instruction": system,
            
            "response_mime_type": response_mime_type,
            "response_schema": response_schema,
            
            "max_output_tokens": model_config.max_tokens,
            "temperature": model_config.temperature,
            "top_p": model_config.top_p,
            "top_k": model_config.top_k,
            "frequency_penalty": model_config.frequency_penalty,
            "presence_penalty": model_config.presence_penalty,
            }
        )
        
        return response
    
    def generate(
        self, 
        model_config: ModelConfig,
        contents: List[Message] | str, 
        system: Optional[str] = None, 
        structured_schema: Optional[Type[BaseModel]] = None,
        store_config: bool = False
        ) -> LLMResponse:
        """Generate a text response from Google Gemini"""
        resp = self.__generate(model_config, contents, system, structured_schema)
        
        prompt_token_count = resp.usage_metadata.prompt_token_count or 0 if resp.usage_metadata else 0
        completion_token_count = resp.usage_metadata.candidates_token_count or 0 if resp.usage_metadata else 0
        total_token_count = resp.usage_metadata.total_token_count or 0 if resp.usage_metadata else 0
        
        return LLMResponse(
            resp=resp.text, 
            usage=UsageMetadata(
                prompt_tokens=prompt_token_count,
                completion_tokens=completion_token_count,
                total_tokens=total_token_count
            ),
            model_config=model_config if store_config else None
        )
    
    def generate_structured(
        self, 
        model_config: ModelConfig,
        contents: List[Message] | str, 
        system: Optional[str] = None, 
        structured_schema: Optional[Type[BaseModel]] = None,
        store_config: bool = False
        ) -> LLMResponse:
        """Generate a structured response from Google Gemini"""
        resp = self.__generate(model_config, contents, system, structured_schema)
        
        prompt_token_count = resp.usage_metadata.prompt_token_count or 0 if resp.usage_metadata else 0
        completion_token_count = resp.usage_metadata.candidates_token_count or 0 if resp.usage_metadata else 0
        total_token_count = resp.usage_metadata.total_token_count or 0 if resp.usage_metadata else 0
        
        return LLMResponse(
            resp=resp.parsed,
            usage=UsageMetadata(
                prompt_tokens=prompt_token_count,
                completion_tokens=completion_token_count,
                total_tokens=total_token_count
            ),
            model_config=model_config if store_config else None
        )
    
    def generate_chat(
        self, 
        model_config: ModelConfig,
        messages: List[Message],
        system: Optional[str] = None,
        structured_schema: Optional[Type[BaseModel]] = None,
        store_config: bool = False,
        **kwargs: Any) -> Any:
        """Generate a chat response from Google Gemini"""
        
        raise NotImplementedError("Chat generation is not supported for google")



class AnthropicClient(LLMClient):
    """
    Anthropic client
    
    TODO: Anthropic supports tool calling - https://docs.anthropic.com/en/api/messages#body-tool-choice
    TODO: citations (beta?)
    TODO: token streaming - https://docs.anthropic.com/en/api/messages-streaming
    TODO: Chat
    """
    
    def __init__(self, client: anthropic.Anthropic):
        super().__init__(client)
        self.client: anthropic.Anthropic
        
    def __generate(
        self, 
        model_config: ModelConfig,
        contents: List[Message] | str, 
        system: Optional[str] = None, 
        structured_schema: Optional[Type[BaseModel]] = None,
        ) -> anthropic.types.Message:
        """Generate a text response from Anthropic"""
            
        if isinstance(contents, str):
            anthropic_contents = [MessageParam(role="user", content=contents)]
        else:
            anthropic_contents = [MessageParam(role=m.role, content=m.content) for m in contents]
        
        if structured_schema:
            raise NotImplementedError("Structured schema is not supported for anthropic")
        
        return self.client.messages.create(
            model=model_config.model,
            max_tokens=model_config.max_tokens,
            messages=anthropic_contents,
            system=system if system else "",
            temperature=model_config.temperature if model_config.temperature else anthropic.NOT_GIVEN,
            top_p=model_config.top_p if model_config.top_p else anthropic.NOT_GIVEN,
            top_k=model_config.top_k if model_config.top_k else anthropic.NOT_GIVEN,
            stop_sequences=model_config.stop_sequences if model_config.stop_sequences else anthropic.NOT_GIVEN,
        )
    
    def generate(
        self, 
        model_config: ModelConfig,
        contents: List[Message] | str, 
        system: Optional[str] = None, 
        structured_schema: Optional[Type[BaseModel]] = None,
        store_config: bool = False
        ) -> LLMResponse:
        """Generate a text response from Anthropic"""
        resp = self.__generate(model_config, contents, system, structured_schema)
        
        resp_content = resp.content[0].text if resp.content[0].type == "text" else None
        
        return LLMResponse(
            resp=resp_content,
            usage=UsageMetadata(
                prompt_tokens=resp.usage.input_tokens,
                completion_tokens=resp.usage.output_tokens,
                total_tokens=resp.usage.input_tokens + resp.usage.output_tokens
            ),
            model_config=model_config if store_config else None
        )
        
    def generate_structured(
        self, 
        model_config: ModelConfig,
        contents: List[Message] | str, 
        system: Optional[str] = None, 
        structured_schema: Optional[Type[BaseModel]] = None,
        store_config: bool = False
        ) -> LLMResponse:
        """Generate a structured response from Anthropic"""
        raise NotImplementedError("Structured schema is not supported for anthropic")
        
    def generate_chat(
        self, 
        model_config: ModelConfig,
        messages: List[Message],
        system: Optional[str] = None,
        structured_schema: Optional[Type[BaseModel]] = None,
        store_config: bool = False,
        **kwargs: Any) -> Any:
        """Generate a chat response from Anthropic"""
        
        raise NotImplementedError("Chat generation is not supported for anthropic")
