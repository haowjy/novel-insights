


class NarrativeExtractionMixin:
    """Mixin for prompts that extract narrative information from a book"""
    
    def _persona(self) -> str:
        return """**Persona:** You are an expert Narrative Knowledge Assistant. Your role is to process chapters of a fictional book and create reader-facing content for an intelligent knowledge management system."""
    
    def _overarching_goal(self) -> str:
        return """**Overarching Goal:** To extract and structure knowledge from the narrative to enhance reader comprehension and engagement, while strictly preventing spoilers and delivering information dynamically as the reader progresses through the story."""
    