
import json
from pathlib import Path
import os
from novelinsights.schemas.prompt_responses.narrative.chapterbychapter.find_entities import FindEntitiesOutputSchema
from novelinsights.schemas.prompt_responses.narrative.chapterbychapter.upsert_entities import UpsertEntitiesOutputSchema
from novelinsights.services.ai.llmclient import LLMResponse
from novelinsights.services.ai.prompts import (
    FindEntitiesPrompt, FindEntitiesTemplate,
    SummarizeChapterPrompt, SummarizeChapterTemplate,
    UpsertEntitiesPrompt, UpsertEntitiesTemplate
)
from novelinsights.utils.mocks.mock_story import MockStory, load_story

def mock_out_path(story_path: Path, chapter_index: int, file_name: str) -> Path:
    return story_path / f"chapter_{chapter_index}-out/{file_name}"

# ------------------------------------------------------------------------------------------------
#
# SUMMARIZE
#
# ------------------------------------------------------------------------------------------------


def load_mock_summarize(story: MockStory, chapter_index: int) -> LLMResponse:
    story_path = story.metadata.story_path
    with open(mock_out_path(story_path, chapter_index, "summarize.json"), "r") as f:
        json_dict = json.load(f)
    summarize_response = LLMResponse(resp=json_dict.get("resp"), usage=json_dict.get("usage"))
    return summarize_response

def load_mock_summarize_prompt(story: MockStory, chapter_index: int) -> SummarizeChapterPrompt:
    summarize_prompt_template = SummarizeChapterTemplate(
        story_title=story.metadata.story_title,
        genres=story.metadata.genres,
        additional_tags=story.metadata.additional_tags,
        story_description=story.metadata.story_description,
        chapter_title=story.chapters[chapter_index].chapter_title,
        chapter_content=story.chapters[chapter_index].chapter_content,
        structured_output_schema=None
    )
    summarize_prompt = SummarizeChapterPrompt(prompt_template=summarize_prompt_template)
    return summarize_prompt

def save_mock_summarize(story: MockStory, chapter_index: int, summarize_resp: LLMResponse):
    story_path = story.metadata.story_path
    with open(mock_out_path(story_path, chapter_index, "summarize.json"), 'w') as f:
        f.write(summarize_resp.to_json_str())
        

# ------------------------------------------------------------------------------------------------
#
# FIND ENTITIES
#
# ------------------------------------------------------------------------------------------------


def load_mock_find_entities(story: MockStory, chapter_index: int) -> LLMResponse:
    story_path = story.metadata.story_path
    with open(mock_out_path(story_path, chapter_index, "find_entities.json"), "r") as f:
        json_dict = json.load(f)

    return LLMResponse.from_dict(json_dict, resp_schema=FindEntitiesOutputSchema)

def load_mock_find_entities_prompt(story: MockStory, chapter_index: int) -> FindEntitiesPrompt:
    find_entities_prompt_template = FindEntitiesTemplate(
        story_title=story.metadata.story_title,
        genres=story.metadata.genres,
        additional_tags=story.metadata.additional_tags,
        story_description=story.metadata.story_description,
        chapter_title=story.chapters[chapter_index].chapter_title,
        chapter_content=story.chapters[chapter_index].chapter_content,
        structured_output_schema=FindEntitiesOutputSchema
    )
    find_entities_prompt = FindEntitiesPrompt(prompt_template=find_entities_prompt_template)
    return find_entities_prompt

def save_mock_find_entities(story: MockStory, chapter_index: int, find_entities_resp: LLMResponse):
    story_path = story.metadata.story_path
    with open(mock_out_path(story_path, chapter_index, "find_entities.json"), 'w') as f:
        f.write(find_entities_resp.to_json_str())
        
# ------------------------------------------------------------------------------------------------
#
# Upsert Entities
#
# ------------------------------------------------------------------------------------------------

def load_mock_upsert_entities(story: MockStory, chapter_index: int) -> list[LLMResponse[UpsertEntitiesOutputSchema]]:
    story_path = story.metadata.story_path
    
    file_names = [f"upsert_entities_{i}" for i in os.listdir(mock_out_path(story_path, chapter_index, "")) if i.startswith("upsert_entities")]
    responses = []
    for file_index in range(len(file_names)):
        with open(mock_out_path(story_path, chapter_index, f"upsert_entities_{file_index}.json"), "r") as f:
            json_dict = json.load(f)
            responses.append(LLMResponse.from_dict(json_dict, resp_schema=UpsertEntitiesOutputSchema))
    return responses

def load_single_mock_upsert_entities(story: MockStory, chapter_index: int, file_index: int) -> LLMResponse[UpsertEntitiesOutputSchema]:
    story_path = story.metadata.story_path
    with open(mock_out_path(story_path, chapter_index, f"upsert_entities_{file_index}.json"), "r") as f:
        json_dict = json.load(f)
        return LLMResponse.from_dict(json_dict, resp_schema=UpsertEntitiesOutputSchema)

def load_mock_upsert_entities_prompt(story: MockStory, chapter_index: int) -> UpsertEntitiesPrompt:
    upsert_entities_template = UpsertEntitiesTemplate(
        story_title=story.metadata.story_title,
        genres=story.metadata.genres,
        additional_tags=story.metadata.additional_tags,
        story_description=story.metadata.story_description,
        chapter_title=story.chapters[chapter_index].chapter_title,
        chapter_content=story.chapters[chapter_index].chapter_content,
        new_entities=[],
        structured_output_schema=UpsertEntitiesOutputSchema
    )
    upsert_entities_prompt = UpsertEntitiesPrompt(prompt_template=upsert_entities_template)
    return upsert_entities_prompt

def save_mock_upsert_entities(story: MockStory, chapter_index: int, upsert_entities_resp: LLMResponse[UpsertEntitiesOutputSchema], file_index: int):
    story_path = story.metadata.story_path
    with open(mock_out_path(story_path, chapter_index, f"upsert_entities_{file_index}.json"), 'w') as f:
        f.write(upsert_entities_resp.to_json_str())

if __name__ == "__main__":
    story = load_story()
    print(story)
    
    summarize_response = load_mock_summarize(story, 0)
    print(summarize_response.resp)
    print(summarize_response.usage)