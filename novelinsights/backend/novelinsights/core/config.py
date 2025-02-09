# novelinsights/backend/novelinsights/core/config.py

from dataclasses import field, dataclass
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
    max_tokens: int = field(default=1000)
    temperature: float = field(default=0.5)
    top_p: float = field(default=1.0)
    top_k: int = field(default=10)
    frequency_penalty: float = field(default=0.0)
    presence_penalty: float = field(default=0.0)
    repetition_penalty: float = field(default=1.0)
    stop_sequences: list[str] = field(default_factory=list)
    