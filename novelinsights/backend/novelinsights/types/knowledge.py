from novelinsights.types.base import DescribedEnum

#
# Knowledge Graph
#
#
class NodeType(DescribedEnum):
    # Entities and Groups
    CHARACTER = ("character", "Names of important people, beings, or sentient entities")
    ORGANIZATION = ("organization", "Important groups that can be described as a collection of characters")
    
    LOCATION = ("location", "Important places or spaces")
    ITEM = ("item", "Important physical or abstract objects (e.g. weapons, artifacts, technologies)")
    CONCEPT = ("concept", "Important ideas, systems, powers, theories")
    CULTURE = ("culture", "Distinct societal patterns/practices")
    
    # Temporal
    EVENT = ("event", "Significant events, occurrences")
    TIME_PERIOD = ("time_period", "Important temporal ranges")
    
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
    MEMBERSHIP = ("membership", "Being part of organization/group")
    LEADERSHIP = ("leadership", "Leading/commanding others")
    ALLIANCE = ("alliance", "Alliances between groups/entities")
    
    # Spatial/Physical
    LOCATION = ("location", "Physical relationships (contains, near)")
    POSSESSION = ("possession", "Ownership/possession relationships")
    
    # Abstract/Other
    KNOWLEDGE = ("knowledge", "Knowledge/awareness relationships")
    INFLUENCE = ("influence", "Impact/effect relationships")
    CAUSATION = ("causation", "Cause-effect relationships")
    OTHER = ("other", "Other types")

class RelationStatusType(DescribedEnum):
    ACTIVE = ("active", "Currently valid relationship")
    DORMANT = ("dormant", "Temporarily inactive (e.g., characters separated)")
    BROKEN = ("broken", "Explicitly ended (e.g., breakup, betrayal)")
    DECEASED = ("deceased", "One party died")
    HISTORICAL = ("historical", "Past relationship, no longer current")
    UNKNOWN = ("unknown", "Status unclear or not specified")
