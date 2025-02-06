# novelinsights/models/__init__.py
from novelinsights.models.base import Base
from novelinsights.models.core.user import User
from novelinsights.models.content.content_unit import ContentUnit
from novelinsights.models.content.context import Context
from novelinsights.models.content.structure import ContentStructure
from novelinsights.models.knowledge.node import Node, NodeState
from novelinsights.models.knowledge.relationship import NodeRelationship, NodeRelationshipState
from novelinsights.models.metadata.agent_metadata import AgentMetadata
from novelinsights.models.metadata.prompt_metadata import PromptMetadata
from novelinsights.models.presentation.article import Article, ArticleSnapshot

# This ensures all models are registered
__all__ = [
    "Base",
    "User",
    "ContentUnit",
    "Context",
    "ContentStructure",
    "Node",
    "NodeState",
    "NodeRelationship",
    "NodeRelationshipState",
    "AgentMetadata",
    "PromptMetadata",
    "Article",
    "ArticleSnapshot"
]