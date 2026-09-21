NOTE_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "create_note",
            "description": "Create a new note with a title and content.",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {
                        "type": "string",
                        "description": "Short and concise title of the note.",
                    },
                    "content": {
                        "type": "string",
                        "description": "Full text body or content of the note.",
                    },
                },
                "required": ["title", "content"],
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "list_notes",
            "description": "Retrieve all stored notes.",
            "parameters": {
                "type": "object",
                "properties": {},
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "search_notes",
            "description": "Search notes by keyword in their title or content.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search keyword or phrase to look for.",
                    }
                },
                "required": ["query"],
                "additionalProperties": False,
            },
        },
    },
]
