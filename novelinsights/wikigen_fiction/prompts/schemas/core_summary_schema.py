schema = {
  "type": "object",
  "properties": {
    "genres": {
        "type": "array",
        "items": {
            "type": "string",
            "description": "The genre(s) of the story"
        }
    },
    "setting": {
      "type": "string",
      "description": "Description of the primary setting or world in which the story takes place"
    },
    "overall_summary": {
      "type": "string",
      "description": "A detailed summary of the entire story so far, highlighting the main plot developments. For longer descriptions, use markdown with headers and subheaders to organize."
    },
    "plot_overview": {
      "type": "array",
      "description": "A list of key arcs spanning multiple chapters",
      "items": {
        "type": "object",
        "properties": {
          "arc_name": {
            "type": "string",
            "description": "A concise name or title for the arc"
          },
          "description": {
            "type": "string",
            "description": "A summary of the arc's storyline, including main events and primary conflicts"
          },
          "status": {
            "type": "string",
            "enum": ["ongoing", "complete"],
            "description": "The current status of the arc"
          }
        },
        "required": ["arc_name", "description", "status"]
      }
    }
  },
  "required": ["genres", "setting", "overall_summary", "plot_overview"],
  "additionalProperties": False
}