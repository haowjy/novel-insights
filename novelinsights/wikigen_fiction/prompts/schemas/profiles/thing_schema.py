schema = {
  "type": "object",
  "properties": {
    "name": {
      "type": "string",
      "description": "The primary name or identifier of the object"
    },
    "item_type": {
      "type": "string",
      "description": "The category or type of the object (e.g., weapon, artifact, technology)"
    },
    "aliases": {
      "type": "array",
      "items": {
        "type": "string"
      },
      "description": "Alternative names or identifiers for the object"
    },
    "overview": {
      "type": "string",
      "description": "A concise summary of the object, including its key features and general importance"
    },
    "significance": {
      "type": "string",
      "description": "The object's importance to the plot and how it impacts the story"
    },
    "description": {
      "type": "object",
      "properties": {
        "appearance": {
          "type": "string",
          "description": "Physical description of the object"
        },
        "properties": {
          "type": "string",
          "description": "Special properties, functions, or capabilities of the object"
        }
      },
      "required": ["appearance"]
    },
    "background": {
      "type": "string",
      "description": "Detailed description of origin, past uses, and significant events involving the object. For longer descriptions, use markdown with headers and subheaders to organize."
    },
    "current_status": {
      "type": "string",
      "description": "The current state, location, or possessor of the object"
    },
    "related_entities": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "name": {"type": "string"},
          "type": {"type": "string"},
          "relation": {"type": "string"},
          "description": {"type": "string"}
        }
      },
      "description": "Characters, locations, or other entities closely associated with the object"
    }
  },
  "required": ["name", "item_type", "overview", "significance"],
  "additionalProperties": False
}