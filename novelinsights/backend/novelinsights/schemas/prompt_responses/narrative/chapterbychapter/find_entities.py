    
from pydantic import BaseModel, Field, field_validator
from typing import List
from novelinsights.types.knowledge import SignificanceLevel, EntityType
        
class FoundEntity(BaseModel):
    brief_description: str = Field(
        description="a brief description of the entity (what the entity is, what it does, etc)")
    
    narrative_significance: str = Field(
        description="the narrative significance of the entity in the context of this chapter")
    
    significance_level: SignificanceLevel = Field(
        description=f"the significance level of the entity to the chapter's plot and the story as a whole\n{SignificanceLevel.all_descriptions()}")
    
    entity_type: EntityType = Field(
        description=f"the type of entity.\n{EntityType.all_descriptions()}")
    
    identifier: str = Field(
        description="the main identifier of the entity that will be used to reference the entity and you believe is unique")

    aliases: List[str] = Field(
        description="all names and other identifiers for the entity")
    
    related_entities: List[str] = Field(
        description="list of entity identifiers that are related to the entity")
    
    @field_validator("significance_level", mode="before")
    def ensure_significance_level_enum(cls, v):
        if isinstance(v, str):
            return SignificanceLevel(v)
        return v
    
    @field_validator("entity_type", mode="before")
    def ensure_entity_type_enum(cls, v):
        if isinstance(v, str):
            return EntityType(v)
        return v
    
    def to_upsert_str(self, sig_related_entities: List[str] | None = None) -> str:
        upsert_str = f"""{self.entity_type.value}: {self.identifier} - {self.significance_level.value}\n\t{self.brief_description}"""
        
        if sig_related_entities:
            upsert_str += f"\n\trelated: {', '.join(sig_related_entities)}"
            
        return upsert_str


class FindEntitiesOutputSchema(BaseModel):
    reasoning: str = Field(
        description="detailed reasoning for all the important entities found in the chapter and how they interact with the story")
    
    entities: List[FoundEntity] = Field(
        description="important entities found in the chapter that carry narrative significance")
