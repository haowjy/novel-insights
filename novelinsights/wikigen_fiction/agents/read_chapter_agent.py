"""This module contains the agent class for to read a single chapter and generate a comprehensive summary and information extraction tasks."""

import logging

from typing import Self
from novelinsights.base.base_agent import BaseAgent
from novelinsights.utils.llm import LLMWrapper
from novelinsights.db import QdrantDB

from novelinsights.wikigen_fiction.models.read_chapter_models import (
    ReadChapterPayload,
    ReadChapterResponse,
)

def task() -> str:
    return """Your task is to produce a comprehensive and detailed summary of the current chapter, as well as extract and organize all significant information into predefined categories. The output should be thorough and suitable for creating Wikipedia-style/fan wiki entries, ensuring that all essential details from the chapter are captured accurately."""


def instructions(unknown_genre=False, prev_chap_context: str = None) -> str:
    instructions = f"""Provide your analysis and created the detailed summary in the following format:

## 1. Non-Plot Content
- Identify if the chapter is for non-plot content (e.g., front matter, acknowledgments, table of contents, etc.)
- If the chapter is non-plot content, you make skip Information Extraction and replace the content with "<SKIPPED-EXTRACTION>"{
'''

### 1.1 Story Metadata
- List the genre(s) of the story
- for each genre, provide:
    - Genre name
    - Description of the genre
    - Why the genre is relevant to the story
    - How the story fits within the genre
    - Any unique elements or themes that define the genre in this story
    - rank how relevant the genre is to the story as very high, high, medium, low, or very low
- List any other relevant metadata about the story''' if unknown_genre else ''}

## 2. Information Extraction

For each category below, extract relevant details from the chapter. Present the information in a clear and organized manner, using bullet points or numbered lists where appropriate.

For all items in each category, make sure to explain why you chose them and how they contribute to the plot of the entire story. Rank the importance of each item as very high, high, medium, low, or very low.

### 2.1 Key Events or Developments
- For each key event or development, provide:
- Name or title of the event
- What happened in great detail (3 sentences or more)
- Who was involved
- Where it took place
- When it occurred (if specified)
- Why it's significant to the plot or character development
- Any immediate consequences or reactions

### 2.2 Plot Elements

#### Main conflict or challenges
- Detailed description of the conflict (3 sentences or more)
- Parties involved
- Stakes or potential consequences

#### Subplots
- Brief description
- How they relate to the main plot

#### Pacing and narrative structure observations
- Tempo of events (fast-paced, slow build, etc.)
- Any non-linear storytelling elements (flashbacks, flash-forwards)

#### Plot twists or surprises
- Description of the twist
- impact on the story

### 2.3 Characters
- For each important character, provide a detailed description. Include (if available):
    - Name
    - Role in the story
    - physical description or notable features
    - personality traits
    - Dialogue style or patterns
    - Actions or role in this chapter
    - Notable abilities or skills
    - Psychological state or development in this chapter
    - Motivations or goals revealed
    - Relationships and interactions with other characters

### 2.4 Setting and World-Building:
    
#### Physical Environment
- List key locations (names, detailed descriptions, significance)
- list notable environmental features (climate, geography, etc.)
- List time period or temporal elements (if significant to the story)

#### Distinctive World Elements
- Technology level or magical elements
- List unique aspects of this world (laws of nature, fictional species, etc.)
- List historical context relevant to the current story
    
#### Societal Structure
- List social, political, and economic systems
- List cultural elements (customs, beliefs, languages)
- List organizations or groups (names, purposes, significance)

### 2.5 Significant Objects, Items, or Technologies
For each significant object, item, or technology:
- Name/Description
- type or category
- Physical characteristics
- Function or purpose
- Who possesses or controls it
- Its importance to the plot or characters
- Any special properties or abilities it confers

### 2.6 Foreshadowing or Symbolism
- Identify any instances of foreshadowing or symbolism
- for each instance, provide:
    - Detailed description
    - How it's presented in the text
    - Potential implications for future events

## 3. General Chapter Summary
- Write a detailed summary of the entire chapter (approximately 300-500 words).
- Focus on key plot developments, character actions and interactions, significant events, and any important revelations.
- Ensure the summary is coherent and logically flows from one point to the next.
- This should not be explicitly for "this chapter" but should be a general summary of the chapter's content.
{'''
## 4. Previous Chapter(s) Summary:
- using the previous chapter context, write a summary of the previous chapter(s) to provide continuity and context for the current chapter.''' if prev_chap_context is not None else ''}"""
    return instructions


def general_reminders() -> str:
    return """- Avoid speculation beyond what's directly supported by the text and previous chapter content/summaries.
- DO NOT explicitly mention "chapter" or "book" in the response. Instead, refer to the content as if it were a standalone piece of information.
- Make sure to follow the exact markdown format and structure provided in the instructions with ALL headings and subheadings including the number of hashes '#' (like ## Information Extraction). If the format is incorrect, you will receive a lower score. If a section is not applicable, you may add a note indicating that, but DO NOT remove the section.
"""


def template(
    chap_num: int,
    title: str,
    content: str,
    story_so_far: str = None,
    prev_chap_context: str = None,
) -> str:
    """Generate a prompt for the read chapter agent.

    Args:
        title (str): title of the chapter
        content (str): content of the chapter
        story_so_far (str, optional): summary of the story so far. Defaults to None.
        prev_chap_context (str, optional): context of the previous chapter. Defaults to None.

    Returns:
        str: full prompt for the read chapter agent
    """
    unknown_genre = chap_num <3
    #
    prompt = f"""You are an AI assistant designed to analyze chapters of fiction.

# Task
{task()}{
    f'''
    
# Story so far:
{story_so_far}''' if story_so_far else ''
}{
    f'''

# Previous Chapter(s) Context:
{prev_chap_context}''' if prev_chap_context else ''
}

# Current Chapter Context:
## Chapter Title: {title}
## Chapter Content: 
---
{content}
---

# Instructions
{instructions(unknown_genre, prev_chap_context)}

# General Reminders
{general_reminders()}"""
    return prompt

class ReadChapterAgent(BaseAgent):
    """Agent class for generating a single chapter summary and information extraction tasks."""

    def __init__(self, llm: LLMWrapper, db: QdrantDB):
        self.response: ReadChapterResponse = None
        self.payload: ReadChapterPayload = None
        super().__init__(llm, db)

    def mock_template(self, chap_num = 1) -> str:
        """Generate a mock template for the single chapter agent."""
        p = template(
            chap_num,
            r"{{title}}",
            r"{{content}}",
            r"<OPT>{{story_so_far}}</OPT>",
            r"<OPT>{{prev_chap_context}}</OPT>",
        )
        logging.debug(f"mock prompt tokens: {self.llm.estimate_tokens(p)}")
        return p

    def get_prompt(
        self,
        chap_num:int,
        title: str,
        content: str,
        story_so_far: str = None,
        prev_chap_context: str = None,
    ) -> str:
        """Generate a prompt for the single chapter agent.

        Args:
            title (str): title of the chapter
            content (str): content of the chapter
            story_so_far (str, optional): summary of the story so far. Defaults to None.
            prev_chap_context (str, optional): context of the previous chapter. Defaults to None.

        Returns:
            str: full prompt for the single chapter agent
        """
        p = template(chap_num, title, content, story_so_far, prev_chap_context)
        return p

    def estimate_tokens(
        self,
        chap_num:int,
        title: str,
        content: str,
        story_so_far: str = None,
        prev_chap_context: str = None,
    ) -> int:
        return super().estimate_tokens(
            self.get_prompt(chap_num, title, content, story_so_far, prev_chap_context)
        )

    def get_response_fields(self) -> dict:
        return ReadChapterResponse.model_fields

    def generate(
        self,
        chap_num: int,
        title: str,
        content: str,
        story_so_far: str = None,
        prev_chap_context: str = None,
    ) -> Self:
        """Generate a response for the single chapter agent.

        Args:
            title (str): title of the chapter
            content (str): content of the chapter
            story_so_far (str, optional): summary of the story so far. Defaults to None.
            prev_chap_context (str, optional): context of the previous chapter. Defaults to None.

        Returns:
            str: response generated by the single chapter agent
        """
        prompt = self.get_prompt(chap_num, title, content, story_so_far, prev_chap_context)

        resp_str = super().generate(prompt)
        self.response = ReadChapterResponse.from_response(resp_str)
        self.payload = ReadChapterPayload(
            name=title, prompt=prompt, response=self.response, chap_num=chap_num
        )
        return self

    def _mock_generate(
        self,
        response: str,
        chap_num: int,
        title: str,
        content: str,
        story_so_far: str = None,
        prev_chap_context: str = None,
    ) -> Self:
        """Add the response to the agent history without actually calling the LLM. Used for testing.

        Args:
            response (str): response to add to the agent history
            title (str): title of the chapter
            content (str): content of the chapter
            story_so_far (str, optional): summary of the story so far. Defaults to None.
            prev_chap_context (str, optional): context of the previous chapter. Defaults to None.

        Returns:
            ReadChapterResponse: parsed response model
        """
        prompt = self.get_prompt(chap_num, title, content, story_so_far, prev_chap_context)
        super()._mock_generate(prompt, response)
        self.response: ReadChapterResponse = ReadChapterResponse.from_response(response)
        self.payload = ReadChapterPayload(
            name=title, prompt=prompt, response=self.response, chap_num=chap_num
        )
        return self