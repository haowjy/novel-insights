from enum import Enum

class Provider(str, Enum):
    OPENROUTER = "openrouter"
    GEMINI = "gemini"
    ANTHROPIC = "anthropic"
    OPENAI = "openai"