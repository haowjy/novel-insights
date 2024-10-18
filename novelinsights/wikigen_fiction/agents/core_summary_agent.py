from typing import Optional, Self
import json
from pydantic import BaseModel
from qdrant_client import QdrantClient

from novelinsights.base.base_agent import BaseAgent
from novelinsights.utils import parse_json, LLMWrapper

from novelinsights.wikigen_fiction.agents.read_chapter_agent import ReadChapterResponse
from novelinsights.wikigen_fiction.models import CoreSummaryModel, CoreSummaryPayload, CoreSummaryResponse

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
- DO NOT explicitly mention "chapter" or "book" in the response. Instead, refer to the content as if it were a standalone piece of information.
- Make sure to follow the exact format and structure provided in the instructions."""

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
{task()}"""
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
{json.dumps(CoreSummaryModel.to_json_schema())}
```
Make sure to include the backticks with "json" to ensure proper formatting.

# Instructions
---
{instructions()}
---

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

class CoreSummaryAgent(BaseAgent):
    """Agent class for updating the core summary of a story based on a new chapter."""
    def __init__(self, llm: LLMWrapper, db: QdrantClient, book_title:str):
        self.book_title = book_title
        self.response:CoreSummaryResponse = None
        self.payload:CoreSummaryPayload = None
        super().__init__(llm, db)
    
    def mock_template(self) -> str:
        """Generate a mock template for the single chapter agent."""
        return template(r"{{content}}", r"<OPT>{{prev_json}}</OPT>")
    
    def get_prompt(self, content:ReadChapterResponse, prev_json: dict = None) -> str:
        """Generate a prompt for the single chapter agent.
        
        Args:
            content (str): content of the chapter
            prev_json (dict, optional): previous core summary in JSON format. Defaults to None.
        
        Returns:
            str: full prompt for the single chapter agent
        """
        return template(content, prev_json)
        
    def estimate_tokens(self, content:ReadChapterResponse, prev_json: dict = None) -> int:
        return super().estimate_tokens(self.get_prompt(content, prev_json))
    
    def generate(self, content:ReadChapterResponse, prev_json: dict = None) -> Self:
        """Generate a response for the single chapter agent.
        
        Args:
            content (str): content of the chapter
            prev_json (str, optional): previous core summary in JSON format. Defaults to None.
        
        Returns:
            str: response generated by the single chapter agent
        """
        prompt = self.get_prompt(content, prev_json)
        resp_str = super().generate(prompt)
        self.response = CoreSummaryResponse(full_response=resp_str, core_summary_json=parse_json(resp_str))
        self.payload = CoreSummaryPayload(
            name=self.book_title, 
            prompt=prompt, 
            response=self.response
            )
        return self
    
    def _mock_generate(self, response:str, content:ReadChapterResponse, prev_json: dict = None) -> Self:
        """Mock the generate method for testing purposes."""
        prompt = self.get_prompt(content, prev_json)
        super()._mock_generate(prompt, response)
        self.response = CoreSummaryResponse(full_response=response, core_summary_json=parse_json(response))
        self.payload = CoreSummaryPayload(
            name=self.book_title, 
            prompt=prompt, 
            response=self.response
            )
        return self
    