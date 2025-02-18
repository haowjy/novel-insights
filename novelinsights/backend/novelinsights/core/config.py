# novelinsights/backend/novelinsights/core/config.py

from dataclasses import field, dataclass
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        # `.env.prod` takes priority over `.env`
        env_file=('.env', '.env.prod')
    )

@dataclass
class ModelConfig:
    provider: str = field(default="anthropic")
    model: str = field(default="claude-3-5-sonnet-20241022")
    max_tokens: int = field(default=1024)
    
    temperature: Optional[float] = field(default=None)
    top_p: Optional[float] = field(default=None)
    top_k: Optional[int] = field(default=None)
    frequency_penalty: Optional[float] = field(default=None)
    presence_penalty: Optional[float] = field(default=None)
    repetition_penalty: Optional[float] = field(default=None)
    stop_sequences: Optional[list[str]] = field(default=None)
    