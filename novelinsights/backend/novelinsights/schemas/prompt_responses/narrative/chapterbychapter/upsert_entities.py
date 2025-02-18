from pydantic import BaseModel, Field
from typing import List, Optional

from novelinsights.types.knowledge import EntitySignificanceLevel, EntityType, RelationDirectionType, RelationType

class UpsertFact(BaseModel):
    explicit: List[str] = Field(
        description="directly stated in text")
    
    implicit: List[str] = Field(
        description="inferred from the text")
    
    situational: List[str] = Field(
        description="temporary/contextual information")
    
    foundational: List[str] = Field(
        description="core/persistent information")


class UpsertEntity(BaseModel):
    detailed_description: str = Field(
        description="detailed description of the entity")
    
    narrative_significance: str = Field(
        description="why this entity matters in the story and beyond")
    
    significance_level: EntitySignificanceLevel = Field(
        description="significance level of the entity to the story and beyond")
    
    entity_type: EntityType = Field(
        description="type of entity")
    
    identifier: str = Field(
        description="main identifier of the entity that will be used to reference the entity and you believe is unique. you may change the identifier if you think it is no longer unique.")
    
    old_identifier: Optional[str] = Field(
        description="old identifier of the entity if you are updating an existing entity")
    
    facts: UpsertFact = Field(
        description="important facts about the entity")
    
    history: List[str] = Field(
        description="detailed chronology of important history of the entity")

    aliases: List[str] = Field(
        description="all names and other identifiers for the entity")
    
    related_entities: List[str] = Field(
        description="identifiers of other entities that are related to the entity")


class UpsertRelationship(BaseModel):
    description: str = Field(
        description="description of the relationship's current state")
    
    source_entity: str = Field(
        description="source entity")
    
    target_entity: str = Field(
        description="target entity")
    
    relationship_type: RelationType = Field(
        description="type of relationship between the source and target entities")
    
    relationship_direction: RelationDirectionType = Field(
        description="direction of the relationship between the source and target entities")
    
class UpsertEntitiesOutputSchema(BaseModel):
    entities: List[UpsertEntity] = Field(
        description="important entities found in the chapter that carry narrative significance")
    
    relationships: List[UpsertRelationship] = Field(
        description="relationships between the entities")
