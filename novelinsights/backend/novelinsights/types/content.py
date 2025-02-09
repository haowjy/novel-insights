from novelinsights.types.base import DescribedEnum


class ContentStructureType(DescribedEnum):
    # Narrative Structure (canonical book content)
    BOOK = ("book", "A complete work of literature")
    VOLUME = ("volume", "A collection of chapters")
    ARC = ("arc", "A collection of chapters that form a larger narrative arc")
    CHAPTER = ("chapter", "A single chapter of a book")
    SCENE = ("scene", "A single scene of a chapter")
    PASSAGE = ("passage", "A single passage of a chapter")
    
    # Supplementary Content
    WIKI_ENTRY = ("wiki_entry", "A wiki entry for a character, location, or concept")
    WORLDBUILDING = ("worldbuilding", "Worldbuilding elements")
    CHARACTER_SHEET = ("character_sheet", "A character sheet for a character")
    PLOT_OUTLINE = ("plot_outline", "A plot outline for a work")
    
    # Generic Structure Types
    PROJECT = ("project", "A project is a collection of content structures")
    COLLECTION = ("collection", "A collection is a collection of content structures")
    TIMELINE = ("timeline", "A timeline is a collection of content structures")
    
    OTHER = ("other", "Other types not listed above")
    
    # TODO: idk if we need these
    # Other Types of Structures
    # POEM = "poem"
    # SONG = "song"
    # PLAY = "play"
    # MOVIE = "movie"
    # TV_SHOW = "tv_show"
    # GAME = "game"



class ContextScope(DescribedEnum):
    GLOBAL = ("global", "Applies to entire work")
    STRUCTURAL = ("structural", "Applies to specific content structures")
    CONTENT_UNIT = ("content_unit", "Applies to specific content units")

class ContextType(DescribedEnum):
    THEME = ("theme", "Recurring ideas or motifs")
    POV = ("pov", "Point of view")
    AUTHOR_NOTE = ("author_note", "Author's notes or insights")
    WORLDBUILDING = ("worldbuilding", "Worldbuilding elements")
    WRITING_GUIDANCE = ("writing_guidance", "Guidance for writing the work")
    OTHER = ("other", "Other types not listed above")


