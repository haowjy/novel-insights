from pydantic import Field

class ReasoningMixin:
    reasoning: str = Field(...,
        description="Explain the step-by-step thought process behind the provided values. Include key considerations and how they influenced the final decisions."
    )