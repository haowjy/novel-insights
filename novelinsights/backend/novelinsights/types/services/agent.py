from novelinsights.types.base import DescribedEnum

from typing import Type

class AgentType(DescribedEnum):
    Base = ("base", "Base agent type")
    # ENTITY_ANALYZER = "entity_analyzer"
    # SUMMARIZER = "summarizer"
    # RELATIONSHIP_ANALYZER = "relationship_analyzer"
    # CLASSIFIER = "classifier"
    
    def get_agent_class(self) -> Type:
        """Get the agent class for this type"""
        # from .entity_analyzer import EntityAnalyzerAgent
        # from .summarizer import SummarizerAgent
        # from .relationship_analyzer import RelationshipAnalyzerAgent
        # from .implementations.classifier import ClassifierAgent
        
        # agent_map = {
        #     AgentType.ENTITY_ANALYZER: EntityAnalyzerAgent,
        #     AgentType.SUMMARIZER: SummarizerAgent,
        #     AgentType.RELATIONSHIP_ANALYZER: RelationshipAnalyzerAgent,
        #     AgentType.CLASSIFIER: ClassifierAgent,
        # }
        # return agent_map[self]
        # TODO: Implement this
        raise NotImplementedError(f"TODO: Implement Agent class for {self}")