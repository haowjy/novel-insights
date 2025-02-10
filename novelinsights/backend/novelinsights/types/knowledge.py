from novelinsights.types.base import DescribedEnum

#
# Knowledge Graph
#
#
class NodeType(DescribedEnum):
    
    # Temporal
    EVENT = ("event", "Significant events, occurrences")
    TIME_PERIOD = ("time_period", "Significant temporal ranges")
    
    # Entities and Groups
    CHARACTER = ("character", "Significant people, beings, or sentient entities, (including unnamed characters)")
    ORGANIZATION = ("organization", "Significant groups that can be described as a collection of characters")
    
    LOCATION = ("location", "Significant places or spaces, (including unnamed locations)")
    ITEM = ("item", "Significant physical or abstract objects (e.g. weapons, artifacts, technologies)")
    CONCEPT = ("concept", "Significant ideas, systems, powers, theories")
    CULTURE = ("culture", "Significant societal patterns/practices")
    
    # Narrative
    ARC = ("arc", "Major narrative progressions")
    THEME = ("theme", "Recurring ideas or motifs")
    
    OTHER = ("other", "Other types not listed above")



class RelationDirectionType(DescribedEnum):
    OUTBOUND = ("outbound", "Relationship from source to target")
    INBOUND = ("inbound", "Relationship from target to source")
    BIDIRECTIONAL = ("bidirectional", "Mutual relationship")

class RelationType(DescribedEnum):
    # Social/Personal
    FAMILY = ("family", "Family relationships")
    FRIENDSHIP = ("friendship", "Friendships")
    RIVALRY = ("rivalry", "Rivalries/enemies")
    ROMANCE = ("romance", "Romantic relationships")
    
    # Organizational
    MEMBERSHIP = ("membership", "Being part of an organization/group")
    LEADERSHIP = ("leadership", "Leading/commanding others")
    ALLIANCE = ("alliance", "Alliances between groups/entities")
    
    # Spatial/Physical
    LOCATION = ("location", "Physical relationships (contains, near, etc.)")
    POSSESSION = ("possession", "Ownership/possession relationships")
    
    # Abstract/Other
    KNOWLEDGE = ("knowledge", "Knowledge/awareness relationships")
    INFLUENCE = ("influence", "Impact/effect relationships")
    CAUSATION = ("causation", "Cause-effect relationships")
    OTHER = ("other", "Other relationship types")

class RelationStatusType(DescribedEnum):
    ACTIVE = ("active", "Currently valid relationship")
    DORMANT = ("dormant", "Temporarily inactive (e.g., characters separated)")
    BROKEN = ("broken", "Explicitly ended (e.g., breakup, betrayal)")
    DECEASED = ("deceased", "One party died")
    HISTORICAL = ("historical", "Past relationship, no longer current")
    UNKNOWN = ("unknown", "Status unclear or not specified")
