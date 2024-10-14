schema = {
  "type": "object",
  "properties": {
    "name": {
      "type": "string",
      "description": "The official name of the organization"
    },
    "aliases": {
      "type": "array",
      "items": {
        "type": "string"
      },
      "description": "Alternative names or nicknames for the organization"
    },
    "overview": {
      "type": "string",
      "description": "A concise summary of the organization, its purpose, role in the story, and current goals"
    },
    "significance": {
      "type": "string",
      "description": "The organization's importance to the plot and its impact on the story world"
    },
    "background": {
      "type": "string",
      "description": "Detailed history and lore of the location. For longer descriptions, use markdown with headers and subheaders to organize."
    },
    "key_members": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "name": {"type": "string"},
          "role": {"type": "string"},
          "description": {"type": "string"}
        }
      },
      "description": "Important individuals associated with the organization"
    },
    "connections": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "entity": {"type": "string"},
          "nature": {"type": "string"},
          "description": {"type": "string"}
        }
      },
      "description": "Key relationships with other organizations, groups, or significant characters"
    }
  },
  "required": ["name", "overview", "significance", "background"],
  "additionalProperties": False
}