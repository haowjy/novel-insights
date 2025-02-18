from enum import Enum

class Provider(str, Enum):
    OPENROUTER = "openrouter"
    GOOGLE = "google"
    ANTHROPIC = "anthropic"
    OPENAI = "openai"