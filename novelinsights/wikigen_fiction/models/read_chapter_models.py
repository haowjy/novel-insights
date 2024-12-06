from pydantic import BaseModel, Field
from typing import Literal, Optional

from novelinsights.base.base_wg_fiction_payload import BaseLLMPayload

class ReadChapterExtraction(BaseModel):
    chapter_summary: str
    key_events: Optional[str]
    plot_elements: Optional[str]
    characters: Optional[str]
    world_building: Optional[str]
    items: Optional[str]

class ReadChapterResponse(BaseModel):
    full_response: str
    skipped_info_extraction: bool
    info_extraction: ReadChapterExtraction

    def from_response(response: str) -> "ReadChapterResponse":
        """Parse the LLM response string from the read chapter agent into the response model.

        Args:
            response (str): response from the read chapter agent

        Returns:
            ReadChapterResponse: parsed response model
        """
        skipped_info_extraction = "<SKIPPED-EXTRACTION>" in response
        full_response = response
        
        # Remove ## 1. Non-Plot Content

        split_12_3 = response.partition("## 3.")  ## 3. General Chapter Summary
        chapter_summary = "##" + split_12_3[2]

        if skipped_info_extraction:
            info_extraction = ReadChapterExtraction(chapter_summary=chapter_summary)
        else:
            full_response = "##" + response.partition("## 2.")[2]  #
            split_1_2 = split_12_3[0].partition("## 2.")  # ## 2. Information Extraction
            if split_1_2[2]:
                info_extract = split_1_2[2].strip()
                info_extract = info_extract.split("###")

                key_events = "###" + info_extract[1] if info_extract[1] else None
                plot_elements = "###" + info_extract[2] if info_extract[2] else None
                characters = "###" + info_extract[3] if info_extract[3] else None
                world_building = "###" + info_extract[4] if info_extract[4] else None
                items = "###" + info_extract[5] if info_extract[5] else None

            info_extraction = ReadChapterExtraction(
                key_events=key_events,
                plot_elements=plot_elements,
                characters=characters,
                world_building=world_building,
                items=items,
                chapter_summary=chapter_summary,
            )
        return ReadChapterResponse(
            full_response=full_response,
            skipped_info_extraction=skipped_info_extraction,
            info_extraction=info_extraction,
            chapter_summary=chapter_summary,
        )

# Qdrant Payload to store
class ReadChapterPayload(BaseLLMPayload):
    """Read Chapter Payload Model"""

    type: Literal["read_chapter"] = "read_chapter"
    response: ReadChapterResponse
    chap_num: int
