schema = {
    "type": "object",
    "properties": {
        "name": {
            "type": "string",
            "description": "The primary name of the location"
        },
        "aliases": {
            "type": "array",
            "items": {
                "type": "string"
            },
            "description": "Alternative names or designations for the location"
        },
        "overview": {
            "type": "string",
            "description": "A concise summary of the location, including its type (e.g., city, country, planet), basic characteristics, and general significance"
        },
        "significance": {
            "type": "string",
            "description": "The location's importance to the plot and how it impacts the story"
        },
        "setting": {
            "type": "string",
            "description": "Comprehensive description of the location's setting, including physical characteristics like layout, terrain, climate, and notable features and for cities, this can include urban planning, architecture, and districts. Also include descriptions about the society like the location's inhabitants, governance, culture, and economy. For longer descriptions, use markdown with headers and subheaders to organize."
        },
        "key_features": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "Name of the key feature"
                    },
                    "description": {
                        "type": "string",
                        "description": "Detailed description of the feature and its significance"
                    }
                },
                "required": [
                    "name",
                    "description"
                ]
            },
            "description": "List of notable or unique features of the location"
        },
        "background": {
            "type": "string",
            "description": "Detailed history and lore of the location. For longer descriptions, use markdown with headers and subheaders to organize."
        },
        "nearby": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "Name of the nearby location"
                    },
                    "distance": {
                        "type": "string",
                        "description": "Approximate distance and direction from the main location"
                    },
                    "connection": {
                        "type": "string",
                        "description": "Brief description of the relationship or relevance to the main location"
                    }
                },
                "required": [
                    "name",
                    "distance"
                ]
            },
            "description": "List of nearby locations and their connections to the main location"
        }
    },
    "required": [
        "name",
        "overview",
        "significance",
        "description",
        "background"
    ],
    "additionalProperties": False
}