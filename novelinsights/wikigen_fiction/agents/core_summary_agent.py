from typing import Optional
import json
from pydantic import BaseModel

from novelinsights.base.base_agent import BaseAgent
from novelinsights.base.base_llm import LLMWrapper
from novelinsights.utils import parse_json

from novelinsights.wikigen_fiction.agents.read_chapter_agent import ReadChapterResponse
from novelinsights.wikigen_fiction.prompts.schemas import core_summary_schema

def task() -> str:
    return """Your task is to read the provided summary of the chapter of the story and update the core summary according to the provided JSON schema. The updated summary should accurately reflect the story progression up to the current chapter, ensuring consistency and coherence with previous information, but changing or adding details as necessary."""

def instructions() -> str:
    instructions = """## Understand Chapter Summary
1. Analyze the provided chapter summary to understand the key events, character developments, and plot progression. Determine how the new chapter fits into the overall story.
2. Identify any new characters, locations, or concepts introduced in the chapter.

## Update Core Summary
1. Identify any changes or additions to the core summary based on the new chapter content.
2. Update the core summary with the new information, ensuring that it accurately reflects the story progression up to the current chapter.
3. Ensure consistency and coherence with the existing core summary and previous chapter summaries.
4. Specifically for the major arc, ensure that the arc name can be used for future reference and that the arc description is accurate and comprehensive. 
"""
    return instructions

def general_reminders() -> str:
    return """- Do not use external knowledge or information beyond what is provided in the chapter and previous context.
- Stick strictly to the information in the chapter context and prior story summaries.
- DO NOT explicitly mention "chapter" or "book" in the response. Instead, refer to the content as if it were a standalone piece of information."""

def template(content:ReadChapterResponse, prev_json:dict=None) -> str:
    """Generate a prompt for the read chapter agent.

    Args:
        content (str): content of the chapter
        prev_json (dict, optional): previous core summary in JSON format. Defaults to None.

    Returns:
        str: full prompt for the read chapter agent
    """
    #
    prompt = f"""# Task
{task()}

# Instructions
{instructions()}"""
    #
    if prev_json is not None:
      prompt+=f"""
# Previous Core Summary
```json
{json.dumps(prev_json)}
```
"""
    else:
      prompt+=f"""
# Previous Core Summary
(No previous core summary)
"""
    #
    prompt+=f"""
# Chapter Summary
---
{content.full_response}
---

# JSON Schema for Core Summary

```json
{core_summary_schema}
```
Make sure to include the backticks with "json" to ensure proper formatting.

# General Reminders
{general_reminders()}"""
    #
    return prompt

# Chain of Thought???
# # Output Instructions
# - Think step-by-step about how the new chapter content should be integrated into the core summary.
# - Update the core summary with the new information, ensuring that it accurately reflects the story progression up to the current chapter.
# - After thinking through the changes, write the updated core summary in JSON format surrounded by backticks (```json).
# - Ensure that the JSON format is correct and follows the following schema: {core_summary_schema}

# ## Example:
# ---
# 1. Step 1...
# 2. ...
# ...
# N. Core Summary:
# ```json
# (ensure correct schema)
# ```
# ---

class CoreSummaryResponse(BaseModel):
    """Core Summary Response Model"""
    full_response: str
    core_summary_json: Optional[dict] = None

class CoreSummaryAgent(BaseAgent):
    """Agent class for updating the core summary of a story based on a new chapter."""
    def __init__(self, llm: LLMWrapper):
        super().__init__(llm)
    
    def mock_template(self) -> str:
        """Generate a mock template for the single chapter agent."""
        return template(r"{{content}}", r"<OPT>{{prev_json}}</OPT>")
    
    def prompt(self, content:ReadChapterResponse, prev_json: dict = None) -> str:
        """Generate a prompt for the single chapter agent.
        
        Args:
            content (str): content of the chapter
            prev_json (dict, optional): previous core summary in JSON format. Defaults to None.
        
        Returns:
            str: full prompt for the single chapter agent
        """
        return template(content, prev_json)
        
    def estimate_response_tokens(self, content:ReadChapterResponse, prev_json: dict = None) -> int:
        return super().estimate_response_tokens(self.prompt(content, prev_json))
    
    def generate_response(self, content:ReadChapterResponse, prev_json: dict = None) -> CoreSummaryResponse:
        """Generate a response for the single chapter agent.
        
        Args:
            content (str): content of the chapter
            prev_json (str, optional): previous core summary in JSON format. Defaults to None.
        
        Returns:
            str: response generated by the single chapter agent
        """
        resp_str = self.llm.generate_response(self.prompt(content, prev_json))
        self.last_response = CoreSummaryResponse(full_response=resp_str, core_summary_json=parse_json(resp_str))
        self.resp_history.append(self.last_response)
        return self.last_response