from enum import Enum
import json
from typing import Iterator

from novelinsights.schemas.prompt_responses.narrative.chapterbychapter.find_entities import FindEntitiesOutputSchema, FoundEntity
from novelinsights.services.ai.llmclient import LLMResponse
from novelinsights.types.knowledge import SignificanceLevel

# I want to be able to iterate over the entities, skip the ones that are not significant, and in chunks of 5 so the output context window is not exceeded
class KeyEntities:
    
    def __init__(self, entities: list[FoundEntity]):
        self.entities = entities
        entities_by_identifier = {entity.identifier: entity for entity in entities}
        
        self.related_entities_by_identifier = {} # entity id -> list of related entities
        for entity in entities:
            for related_entity_id in entity.related_entities:
                if related_entity_id in entities_by_identifier:
                    self.related_entities_by_identifier.setdefault(entity.identifier, []).append(entities_by_identifier.get(related_entity_id))
    
    def get_all_entity_identifiers(self, min_sig_level: SignificanceLevel = SignificanceLevel.SUPPORTING) -> list[str]:
        entity_identifiers = set(entity.identifier for entity in self.entities if entity.significance_level >= min_sig_level)
                
        for entity in self.related_entities_by_identifier:
            for related_entity in self.related_entities_by_identifier[entity]:
                if related_entity.significance_level >= min_sig_level:
                    entity_identifiers.add(related_entity.identifier)
        
        return list(entity_identifiers)
    
    def get_sig_related_entities_for_upsert(self, entity_id: str, min_sig_level: SignificanceLevel = SignificanceLevel.SUPPORTING) -> list[str]:
        return [entity.identifier for entity in self.related_entities_by_identifier.get(entity_id, []) if entity.significance_level >= min_sig_level]
    
    def yield_for_upsert(self, min_sig_level: SignificanceLevel = SignificanceLevel.SUPPORTING, chunk_size: int = 4) -> Iterator[list[str]]:
        significant_entities: list[str] = []
        for entity in self.entities:
            if entity.significance_level >= min_sig_level:
                significant_entities.append(entity.to_upsert_str(sig_related_entities=self.get_sig_related_entities_for_upsert(entity.identifier, min_sig_level)))
            if len(significant_entities) == chunk_size:
                yield significant_entities
                significant_entities = []
                
        if significant_entities:
            yield significant_entities
    
    def __repr__(self):
        return f"KeyEntities(entities={self.entities})"
    
if __name__ == "__main__":
    
    # TODO: move this to a test
    find_entities_resp: LLMResponse[FindEntitiesOutputSchema] = None # type: ignore

    with open('../../novelinsights/backend/tests/resources/pokemon_amber/chapter_0-out/find_entities.json', 'r') as f:
        json_dict = json.load(f)
        find_entities_resp = LLMResponse.from_dict(json_dict, resp_schema=FindEntitiesOutputSchema)
        
    key_entities = KeyEntities(find_entities_resp.resp.entities)

    print("-" * 100)
    for i, upsert_chunk in enumerate(key_entities.yield_for_upsert(min_sig_level=SignificanceLevel.SUPPORTING, chunk_size=5)):   
        
        for upsert_str in upsert_chunk:
            print(upsert_str)
        print("-" * 100)