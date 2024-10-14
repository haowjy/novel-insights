schema = {
  "type": "object",
  "properties": {
    "term": {
      "type": "string",
      "description": "The primary word or phrase for the concept"
    },
    "category": {
      "type": "string",
      "enum": ["magic_system", "technology", "culture", "politics", "religion", "philosophy", "science", "language", "other"],
      "description": "The general category this concept belongs to"
    },
    "aliases": {
      "type": "array",
      "items": {
        "type": "string"
      },
      "description": "Alternative terms or phrases for this concept"
    },
    "definition": {
      "type": "string",
      "description": "A concise explanation of what the term means"
    },
    "detailed_explanation": {
      "type": "string",
      "description": "A more in-depth explanation of the concept, its nuances, and its significance. Use markdown headers and subheaders for formatting if needed."
    },
    "significance": {
      "type": "string",
      "description": "The importance or impact of this concept on the story, characters, or world"
    },
    "origin": {
      "type": "string",
      "description": "Information about where this concept came from or how it was introduced in the story"
    },
    "related_terms": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "term": {
            "type": "string",
            "description": "A related term or concept"
          },
          "relationship": {
            "type": "string",
            "description": "How this term is related to the main concept"
          }
        },
        "required": ["term"]
      },
      "description": "Other terms or concepts that are closely related or connected"
    },
    "examples": {
      "type": "array",
      "items": {
        "type": "string"
      },
      "description": "Specific examples or instances of the concept being used or applied in the story"
    },
    "first_appearance": {
      "type": "object",
      "properties": {
        "chapter": {
          "type": "number",
          "description": "The chapter number where this concept is first introduced or explained"
        },
        "context": {
          "type": "string",
          "description": "Brief description of how the concept was introduced"
        }
      },
      "required": ["chapter"]
    }
  },
  "required": ["term", "category", "definition", "detailed_explanation"],
  "additionalProperties": False
}