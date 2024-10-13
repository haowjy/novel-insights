# novelinsights.prompts.schemas

# novelinsights.prompts.schemas.profiles
from novelinsights.prompts.schemas.profiles.character_schema import schema as character_schema
from novelinsights.prompts.schemas.profiles.concept_schema import schema as concept_schema
from novelinsights.prompts.schemas.profiles.event_schema import schema as event_schema
from novelinsights.prompts.schemas.profiles.location_schema import schema as location_schema
from novelinsights.prompts.schemas.profiles.organization_schema import schema as organization_schema
from novelinsights.prompts.schemas.profiles.thing_schema import schema as thing_schema

class SchemaManager:
    def __init__(self):
        self.schemas = {
            "character": character_schema,
            "concept": concept_schema,
            "event": event_schema,
            "location": location_schema,
            "organization": organization_schema,
            "thing": thing_schema
        }

    def get_schema(self, profile_type):
        return self.schemas.get(profile_type)

    def __iter__(self):
        for profile_type in self.schemas:
            yield self.schemas[profile_type]