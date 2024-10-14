schema = {
  "type": "object",
  "properties": {
    "name": {
      "type": "string",
      "description": "The entity's primary name or identifier"
    },
    "entity_type": {
      "type": "string",
      "enum": ["character", "monster", "abstract_force"],
      "description": "The type of entity being described"
    },
    "aliases": {
      "type": "array",
      "items": {
        "type": "string"
      },
      "description": "Alternative names or identifiers"
    },
    "overview": {
      "type": "string",
      "description": "A concise summary of the entity, including its essence, role, and key traits"
    },
    "significance": {
      "type": "string",
      "description": "The entity's importance to the plot and how it impacts the story"
    },
    "description": {
      "type": "object",
      "properties": {
        "appearance": {
          "type": "string",
          "description": "Physical description or manifestation of the entity"
        },
        "characteristics": {
          "type": "string",
          "description": "Fundamental traits, behavior patterns, or defining features of the entity"
        },
        "capabilities": {
          "type": "string",
          "description": "Key abilities, powers, or notable effects associated with the entity"
        }
      }
    },
    "background": {
      "type": "string",
      "description": "Detailed description of origins, history, and development of the entity throughout the story. For longer descriptions, use markdown with headers and subheaders to organize."
    },
    "connections": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "name": {"type": "string"},
          "relation": {"type": "string"},
          "description": {"type": "string"}
        }
      },
      "description": "Key relationships or interactions with other entities in the story"
    }
  },
  "required": ["name", "entity_type", "overview", "significance"],
  "additionalProperties": False
}