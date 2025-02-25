from pydantic import BaseModel, Field, field_validator
from typing import List, Optional

from novelinsights.types.knowledge import RelationshipStrength, SignificanceLevel, EntityType, RelationCompositionType, RelationType

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
        description="an extremely detailed summary of the entity (what the entity is, what it does, etc) and its significance to the entire story. Use Markdown formatting to organize this description.")
    
    narrative_significance: str = Field(
        description="the narrative significance of the entity across the entire story so far")
    
    significance_level: SignificanceLevel = Field(
        description=f"significance level of the entity across the entire story\n{SignificanceLevel.all_descriptions()}")
    
    entity_type: EntityType = Field(
        description=f"type of entity.\n{EntityType.all_descriptions()}")
    
    identifier: str = Field(
        description="main identifier of the entity that will be used to reference the entity and you believe is unique. you may change the identifier if you think it is no longer unique.")
    
    old_identifier: Optional[str] = Field(
        description="old identifier of the entity if you are updating an existing entity")
    
    facts: UpsertFact = Field(
        description="facts about the entity that are key to understanding the entity in this story")
    
    history: List[str] = Field(
        description="chronology of the most important history of the entity")

    aliases: List[str] = Field(
        description="all names and other identifiers for the entity")
    
    related_entities: List[str] = Field(
        description="identifiers of other entities that are related to the entity")

    @field_validator("entity_type", mode="before")
    def ensure_entity_type_enum(cls, v):
        if isinstance(v, str):
            return EntityType(v)
        return v
    
    @field_validator("significance_level", mode="before")
    def ensure_significance_level_enum(cls, v):
        if isinstance(v, str):
            return SignificanceLevel(v)
        return v

class UpsertRelationship(BaseModel):
    relationship_type: RelationType = Field(
        description=f"type of relationship between the source and target entity.\n{RelationType.all_descriptions()}")
        
    relationship_composition: RelationCompositionType = Field(
        description=f"composition of the relationship between the source and target entity.")
    
    source_entity: str = Field(
        description="(new) identifier for the source entity")
    
    target_entity: str = Field(
        description="(new) identifier for the target entity")
    
    significance_level: SignificanceLevel = Field(
        description=f"significance level of the relationship across the entire story\n{SignificanceLevel.all_descriptions()}")
    
    strength: RelationshipStrength = Field(
        description=f"strength of the relationship")
    
    current_description: str = Field(
        description="description of the current status of the relationship")
    
    description: str = Field(
        description="detailed description of the relationship across the story")
    
    @field_validator("relationship_type", mode="before")
    def ensure_relationship_type_enum(cls, v):
        if isinstance(v, str):
            return RelationType(v)
        return v
    
    @field_validator("relationship_composition", mode="before")
    def ensure_relationship_composition_enum(cls, v):
        if isinstance(v, str):
            return RelationCompositionType(v)
        return v
    
    @field_validator("significance_level", mode="before")
    def ensure_significance_level_enum(cls, v):
        if isinstance(v, str):
            return SignificanceLevel(v)
        return v
    
    @field_validator("strength", mode="before")
    def ensure_strength_enum(cls, v):
        if isinstance(v, str):
            return RelationshipStrength(v)
        return v
    
    
    
class UpsertEntitiesOutputSchema(BaseModel):
    entities: List[UpsertEntity] = Field(
        description="important entities found in the chapter that carry narrative significance")
    
    relationships: List[UpsertRelationship] = Field(
        description="relationships between the entities")
