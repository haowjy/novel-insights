    
from pydantic import BaseModel, Field
from typing import List
from novelinsights.types.knowledge import EntitySignificanceLevel, EntityType

class FoundEntity(BaseModel):
    description: str = Field(
        description="The description of the entity (what the entity is, what it does, etc)")
    
    narrative_significance: str = Field(
        description="The narrative significance of the entity in the context of this chapter and the story as a whole")
    
    significance_level: EntitySignificanceLevel = Field(
        description="The significance level of the entity to the chapter's plot and the story as a whole")
    
    entity_type: EntityType = Field(
        description="The type of entity")
    
    identifier: str = Field(
        description="The main identifier of the entity that will be used to reference the entity and you believe is unique")

    aliases: List[str] = Field(
        description="All names and other identifiers for the entity")
    
    related_entities: List[str] = Field(
        description="List of entity identifiers that are related to the entity")
    
    def to_upsert_str(self, sig_related_entities: List[str] | None = None) -> str:
        if sig_related_entities:
            return f"""{self.entity_type.value}: {self.identifier} - {self.significance_level.value} (related: {', '.join(sig_related_entities)})"""
        else:
            return f"""{self.entity_type.value}: {self.identifier} - {self.significance_level.value}"""

class FindEntitiesOutputSchema(BaseModel):
    entities: List[FoundEntity] = Field(
        description="important entities found in the chapter that carry narrative significance")
