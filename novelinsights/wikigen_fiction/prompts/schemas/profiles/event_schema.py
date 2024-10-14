schema = {
  "type": "object",
  "properties": {
    "name": {
      "type": "string",
      "description": "The primary name or title of the event"
    },
    "aliases": {
      "type": "array",
      "items": {
        "type": "string"
      },
      "description": "Alternative names or titles for the event"
    },
    "type": {
      "type": "string",
      "enum": ["battle", "political", "personal", "natural disaster", "supernatural", "other"],
      "description": "The category or type of the event"
    },
    "overview": {
      "type": "string",
      "description": "A concise summary of the event, capturing its essence and key points"
    },
    "significance": {
      "type": "string",
      "description": "The event's importance to the plot and its impact on the story and characters"
    },
    "chronology": {
      "type": "string",
      "description": "A sequential account of what happened during the event, including key moments and outcomes. For longer descriptions, use markdown with headers and subheaders to organize."
    },
    "background": {
      "type": "string",
      "description": "Detailed information about the context and lead-up to the event. For longer descriptions, use markdown with headers and subheaders to organize."
    },
    "involved_characters": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "name": {
            "type": "string",
            "description": "Name of the character involved"
          },
          "role": {
            "type": "string",
            "description": "The character's role or involvement in the event"
          }
        },
        "required": ["name"]
      },
      "description": "List of characters who played a significant role in the event"
    },
    "locations": {
      "type": "array",
      "items": {
        "type": "string"
      },
      "description": "Key locations associated with the event"
    },
    "related_events": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "name": {
            "type": "string",
            "description": "Name of the related event"
          },
          "relationship": {
            "type": "string",
            "description": "How this event is related to the main event"
          }
        },
        "required": ["name"]
      },
      "description": "Other events that are directly connected to or influenced by this event"
    }
  },
  "required": ["name", "type", "overview", "significance", "chronology"],
  "additionalProperties": False
}