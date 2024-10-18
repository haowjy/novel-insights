from enum import Enum
from pydantic import BaseModel
from typing import Optional

class PayloadType(Enum):
    core_summary = 'core_summary'
    
    chapter = 'chapter'
    character = 'character'
    location = 'location'
    
    event_timeline = 'event_timeline'
    worldbuilding = 'worldbuilding'
    
    organization = 'organization'
    thing = 'thing'
    concept = 'concept'

    event_chronology = 'event_chronology'
    character_chronology = 'character_chronology'
    
    themes='themes'
    
    
class BasePayload(BaseModel):
    type: Optional[PayloadType]
    name: str

class BaseLLMPayload(BasePayload):
    prompt: str