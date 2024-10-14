from novelinsights.base.base_agent import BaseAgent
from novelinsights.base.base_llm import LLMWrapper

def task() -> str:
    return """Your task is to read the provided chapter of the story and update the long-term summary by extracting and summarizing key information according to the given JSON schema. Focus on identifying major plot developments, updates to main characters, significant events, and key themes introduced or developed in this chapter. The updated summary should accurately reflect the story progression up to the current chapter, ensuring consistency and coherence with previous information."""

def instructions(prev_chap_context:str = None) -> str:
    instructions = """## 1. Information Extraction:
For each category below, extract relevant details from the chapter. Present the information in a clear and organized manner, using bullet points or numbered lists where appropriate. If the chapter does not contain information for a specific category, you may omit it. And if the content of the chapter is not related to the plot (front matter, acknowledgments, table of contents, etc.), you can skip the extraction for that chapter. If you skip the extraction, add <SKIPPED-EXTRACTION> at the beginning of the section.

### Entities:
 - List all important characters introduced or featured in this chapter
 - label them as a character, monster, or abstract force.
 - Provide a detailed description of the character. Include (if available):
 - Name
 - Role in the plot/chapter
 - Personality
 - Relationships with other characters
 - Significant actions or decisions made in the chapter
 - backstory, motivations, or any other relevant details
 - any other relevant details

### Chronology:
 - Identify and list the events that occur or are described in the chapter.
 - MAKE SURE TO INCLUDE A OVERARCHING CONFLICT NAME OR TITLE
     - The overarching conflict is a singular event or theme that ties together the various events in the plot and a major plot point in the story.
 - For each event, provide a detailed description. Include (if available):
 - Name or title of the event
 - Type or category of the event
 - Overarching Conflict name or title
 - Significance to the plot or characters
 - any chronology of the event
 - Background or context leading to the event
 - Characters involved and their roles
 - Locations where the event takes place
 - any other relevant details

### Locations:
 - List and describe any important locations introduced or revisited
 - Provide a detailed description of each location. Include (if available):
 - Name of the location
 - significance to the plot or characters
 - physical description or notable features
 - cultural or historical significance
 - any history or background information
 - nearby locations or connections to other places 
 - any other relevant details

### Organizations:
 - List any important organizations, groups, or factions mentioned or central to the chapter
 - Provide a detailed description of each organization. Include (if available):
 - Name of the organization
 - Purpose or goals
 - Key members or leaders
 - Relationships with other organizations
 - any significant actions or decisions made by the organization
 - any history or background information
 - any other relevant

### Things:
 - List any important items introduced or referenced in the chapter.
 - Provide a detailed description of each item. Include (if available):
 - Name of the item
 - Type or category
 - Physical description or notable features
 - Special properties or functions
 - Significance to the plot or characters
 - History or background information
 - Current status or location
 - any related entities or connections
 - any other relevant details

### Concepts:
 - List any key concepts, ideas, or themes explored in the chapter
 - Provide a detailed description of each concept. Include (if available):
 - Name or title of the concept
 - Definition or explanation
 - Significance to the plot or characters
 - any examples or instances in the chapter
 - any connections to other concepts or themes
 - any other relevant details

## 2. General Chapter Summary:
- Write a detailed summary of the entire chapter (approximately 300-500 words).
- Focus on key plot developments, character actions and interactions, significant events, and any important revelations.
- Ensure the summary is coherent and logically flows from one point to the next.
- This should not be explicitly for "this chapter" but should be a general summary of the chapter's content."""
    if prev_chap_context is not None: instructions += """## 3. Previous Chapter(s) Summary:
- using the previous chapter context, write a summary of the previous chapter(s) to provide continuity and context for the current chapter."""
    return instructions

def general_reminders() -> str:
    return """- Do not use external knowledge or information beyond what is provided in the chapter and previous context.
- Stick strictly to the information in the chapter context and prior story summaries.
- Ensure that any information extracted is directly from the source material and not inferred from outside knowledge.
- Keep responses organized according to the specified structure and formatting instructions.
- Make sure to follow the markdown formatting for clear and readable responses.
- DO NOT explicitly mention "chapter" or "book" in the response. Instead, refer to the content as if it were a standalone piece of information."""

def template(title:str, content:str, story_so_far: str = None, prev_chap_context: str = None) -> str:
    """Generate a prompt for the read chapter agent.

    Args:
        title (str): title of the chapter
        content (str): content of the chapter
        story_so_far (str, optional): summary of the story so far. Defaults to None. 
        prev_chap_context (str, optional): context of the previous chapter. Defaults to None.

    Returns:
        str: full prompt for the read chapter agent
    """
    #
    prompt = f"""# Task
{task()}

# Instructions
{instructions(prev_chap_context)}"""
    #
    if story_so_far is not None:
      prompt+=f"""# Story So Far:
      {story_so_far}
      """
    if prev_chap_context is not None:
        prompt+=f"""# Previous Chapter(s) Context:
        {prev_chap_context}
        """
    #
    prompt+=f"""# Chapter Context:
## Chapter Title: {title}
## Chapter Content: 
---
{content}
---
# General Reminders
{general_reminders()}"""
    #
    return prompt

class ReadChapterAgent(BaseAgent):
    """Agent class for generating a single chapter summary and information extraction tasks."""
    def __init__(self, llm: LLMWrapper):
        super().__init__(llm)
    
    def mock_template(self) -> str:
        """Generate a mock template for the single chapter agent."""
        return template(r"{{title}}", r"{{content}}", r"<OPT>{{story_so_far}}</OPT>", r"<OPT>{{prev_chap_context}}</OPT>")
    
    def prompt(self, title:str, content:str, story_so_far: str = None, prev_chap_context: str = None) -> str:
        """Generate a prompt for the single chapter agent.
        
        Args:
            title (str): title of the chapter
            content (str): content of the chapter
            story_so_far (str, optional): summary of the story so far. Defaults to None.
            prev_chap_context (str, optional): context of the previous chapter. Defaults to None.
        
        Returns:
            str: full prompt for the single chapter agent
        """
        return template(title, content, story_so_far, prev_chap_context)
    
    def generate_response(self, title:str, content:str, story_so_far: str = None, prev_chap_context: str = None) -> str:
        """Generate a response for the single chapter agent.
        
        Args:
            title (str): title of the chapter
            content (str): content of the chapter
            story_so_far (str, optional): summary of the story so far. Defaults to None.
            prev_chap_context (str, optional): context of the previous chapter. Defaults to None.
        
        Returns:
            str: response generated by the single chapter agent
        """
        self.reponse = self.llm.generate_response(self.prompt(title, content, story_so_far, prev_chap_context))
        return self.response
    
    def estimate_response_tokens(self, title:str, content:str, story_so_far: str = None, prev_chap_context: str = None) -> int:
        return super().estimate_response_tokens(self.prompt(title, content, story_so_far, prev_chap_context))
    
    def get_response(self) -> dict:
        """Parse the response from the single chapter agent."""
        
        def skipped_extraction(response:str) -> bool:
            return "<SKIPPED-EXTRACTION>" in response
        
        return {
            "skipped_extraction": skipped_extraction(self.response)
            }