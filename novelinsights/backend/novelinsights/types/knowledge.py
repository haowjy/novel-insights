from enum import Enum, auto
from novelinsights.types.base import DescribedEnum

#
# Knowledge Graph
#
#
       
class EntityType(DescribedEnum):
    # Concrete
    CHARACTER = auto(), "Sentient entities (named or unnamed)"
    ITEM = auto(), "Physical or abstract objects of significance"
    LOCATION = auto(), "Places or spaces of significance"
    
    # Collective
    GROUP = auto(), "Formal or informal collections of characters"
    
    # Abstract/Conceptual
    CONCEPT = auto(), "Abstract ideas, systems, or theories"
    CULTURE = auto(), "Societal patterns, practices, and beliefs"
    
    # Temporal
    TIME_PERIOD = auto(), "Significant temporal ranges"
    
    # Narrative
    ARC = auto(), "the overall shape and progression of a narrative from beginning to end, typically following a pattern of setup, rising conflict, climax, and resolution"
    PLOT_EVENT = auto(), "Pivotal events that significantly alter the narrative's trajectory"
    PLOT_POINT = auto(), "Significant story developments or turning points that drive the plot forward"
    
    # Literary
    SYMBOLISM = auto(), "Symbolic elements and their meanings"
    ALLUSION = auto(), "References to external works/concepts"
    THEME = auto(), "Recurring ideas or motifs"
    
    OTHER = auto(), "Other types not listed above"


class RelationType(DescribedEnum):
    SOCIAL = auto(), "Interpersonal relationships (including familial)"
    ORGANIZATIONAL = auto(), "Institutional or group relationships"
    PHYSICAL = auto(), "Spatial or temporal relationships"
    THEMATIC = auto(), "Narrative, conceptual, or literary relationships"
    CULTURAL = auto(), "Societal and cultural connections"

class RelationCompositionType(DescribedEnum):
    # Basic Structural
    CONTAINS = auto(), "Complete containment/ownership"
    COMPRISES = auto(), "Made up of parts, strong composition"
    AGGREGATES = auto(), "Loose collection of independent entities"
    ASSOCIATES = auto(), "Connected but independent"
    
    # Hierarchical
    SPECIALIZES = auto(), "More specific version of (is-a)"
    GENERALIZES = auto(), "More general version of (is-a)"
    DERIVES_FROM = auto(), "Stems or originates from"
    DEPENDS_ON = auto(), "Requires or needs"
    
    # Narrative Structure
    TRANSFORMS_INTO = auto(), "Becomes or changes into"
    BUILDS_UPON = auto(), "Sequentially develops from"
    MIRRORS = auto(), "Structurally parallels or reflects"
    RESONATES_WITH = auto(), "Creates structural harmony/echo"
    
    # Membership
    BELONGS_TO = auto(), "Member or part of group/whole"
    INCLUDES = auto(), "Has as member or component"
    

class RelationStatusType(DescribedEnum):
    # State
    ACTIVE = auto(), "Currently valid relationship"
    INACTIVE = auto(), "Not currently active but still exists"
    TERMINATED = auto(), "Explicitly ended"
    
    # Development
    DEVELOPING = auto(), "Forming or strengthening"
    TRANSFORMING = auto(), "Changing in nature"
    
    # Certainty
    AMBIGUOUS = auto(), "Status unclear or uncertain"
        
class SignificanceLevel(DescribedEnum):
    CENTRAL = auto(), "crucial to everything"
    MAJOR = auto(), "crucial to current events"
    SUPPORTING = auto(), "actively involved in current events"
    MINOR = auto(), "relevant but not crucial"
    BACKGROUND = auto(), "not important to current events"
    PERIPHERAL = auto(), "mentioned but barely relevant"
    
    def to_int(self) -> int:
        return {self.CENTRAL: 5,self.MAJOR: 4,self.SUPPORTING: 3,self.MINOR: 2,self.BACKGROUND: 1,self.PERIPHERAL: 0,}[self]
    
    def __gt__(self, other: "SignificanceLevel") -> bool:
        return self.to_int() > other.to_int()
    
    def __ge__(self, other: "SignificanceLevel") -> bool:
        return self.to_int() >= other.to_int()
    
    def __lt__(self, other: "SignificanceLevel") -> bool:
        return self.to_int() < other.to_int()
    
    def __le__(self, other: "SignificanceLevel") -> bool:
        return self.to_int() <= other.to_int()

    
class RelationshipStrength(DescribedEnum):
    WEAK = auto(), "Weak relationship"
    MEDIUM = auto(), "Medium relationship"
    STRONG = auto(), "Strong relationship"
    VERY_STRONG = auto(), "Very strong relationship"
    EXTRA_STRONG = auto(), "Extra strong relationship"
    
    def to_int(self) -> int:
        return {self.WEAK: 1,self.MEDIUM: 2,self.STRONG: 3,self.VERY_STRONG: 4,self.EXTRA_STRONG: 5,}[self]
    
    def __gt__(self, other: "RelationshipStrength") -> bool:
        return self.to_int() > other.to_int()
    
    def __ge__(self, other: "RelationshipStrength") -> bool:
        return self.to_int() >= other.to_int()

    def __lt__(self, other: "RelationshipStrength") -> bool:
        return self.to_int() < other.to_int()
    
    def __le__(self, other: "RelationshipStrength") -> bool:
        return self.to_int() <= other.to_int()
