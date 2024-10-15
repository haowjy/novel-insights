# novelinsights.wikigen_fiction.prompts.schemas
from novelinsights.wikigen_fiction.prompts.models.core_summary_model import CoreSummaryModel

# novelinsights.wikigen_fiction.prompts.schemas.profiles
from novelinsights.wikigen_fiction.prompts.models.profiles.character_model import CharacterModel
from novelinsights.wikigen_fiction.prompts.models.profiles.concept_model import ConceptModel
from novelinsights.wikigen_fiction.prompts.models.profiles.event_model import EventModel
from novelinsights.wikigen_fiction.prompts.models.profiles.location_model import LocationModel
from novelinsights.wikigen_fiction.prompts.models.profiles.organization_model import OrganizationModel
from novelinsights.wikigen_fiction.prompts.models.profiles.thing_model import ThingModel

class ModelManager:
    def __init__(self):
        self.models = {
            "core_summary": CoreSummaryModel,
            "character": CharacterModel,
            "concept": ConceptModel,
            "event": EventModel,
            "location": LocationModel,
            "organization": OrganizationModel,
            "thing": ThingModel
        }

    def get_model(self, profile_type):
        return self.models.get(profile_type)

    def __iter__(self):
        for profile_type in self.models:
            yield self.models[profile_type]