from pydantic import BaseModel, Field
from typing import Literal, Optional

from novelinsights.base.base_wg_fiction_payload import BaseLLMPayload

class ReadChapterExtraction(BaseModel):
    chapter_summary: str
    characters: Optional[str]
    chap_events: Optional[str]
    locations: Optional[str]
    organizations: Optional[str]
    things: Optional[str]
    concepts: Optional[str]
    main_conflicts: Optional[str]

class ReadChapterResponse(BaseModel):
    full_response: str
    skipped_info_extraction: bool
    info_extraction: ReadChapterExtraction

    def from_response(response:str) -> "ReadChapterResponse":
        """Parse the LLM response string from the read chapter agent into the response model.

        Args:
            response (str): response from the read chapter agent

        Returns:
            ReadChapterResponse: parsed response model
        """
        full_response = response

        skipped_info_extraction = "<SKIPPED-EXTRACTION>" in response

        split1 = response.split("## General Chapter Summary")
        chapter_summary="## Chapter Summary"+split1[1]

        if skipped_info_extraction:
            info_extraction = ReadChapterExtraction(chapter_summary=chapter_summary)
        else:
            split2 = split1[0].split("## Information Extraction")
            if split2[1]:
                text_extraction=split2[1].strip()

                extract_split = text_extraction.split("###")
                characters = "###"+extract_split[1] if extract_split[1] else None
                chap_events = "###"+extract_split[2] if extract_split[2] else None
                locations = "###"+extract_split[3] if extract_split[3] else None
                organizations = "###"+extract_split[4] if extract_split[4] else None
                things = "###"+extract_split[5] if extract_split[5] else None
                concepts = "###"+extract_split[6] if extract_split[6] else None
                main_conflicts = "###"+extract_split[7] if extract_split[7] else None
            info_extraction = ReadChapterExtraction(characters=characters, 
                                chap_events=chap_events, 
                                locations=locations, 
                                organizations=organizations, 
                                things=things, 
                                concepts=concepts,
                                main_conflicts=main_conflicts,
                                chapter_summary=chapter_summary)
        return ReadChapterResponse(
            full_response=full_response, 
            skipped_info_extraction=skipped_info_extraction, 
            info_extraction=info_extraction, 
            chapter_summary=chapter_summary)

# Qdrant Payload to store
class ReadChapterPayload(BaseLLMPayload):
    """Read Chapter Payload Model"""
    type: Literal["read_chapter"] = "read_chapter"
    response: ReadChapterResponse
    chap_num: int