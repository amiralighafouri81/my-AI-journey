import json
from openai import OpenAI

from app.config import settings
from app.models import NoteCreate
from app.services.note_store import note_store
from app.services.tools import NOTE_TOOLS

SYSTEM_PROMPT = """You are an intelligent AI Assistant with access to a note-taking system.
You can create notes, retrieve existing notes, and search through notes using available tools.

Guidelines:
1. Always call the relevant tool when the user intends to manage or look up notes.
2. Keep your answers concise, accurate, and polite.
3. Match the user's language (reply in Persian if the user prompts in Persian, English otherwise).
"""


class NoteAgent:
    def __init__(self):
        self.client = OpenAI(api_key=settings.openai_api_key)
        self.tools_dispatcher = {
            "create_note": self._tool_create_note,
            "list_notes": self._tool_list_notes,
            "search_notes": self._tool_search_notes,
        }

    def _tool_create_note(self, title: str, content: str) -> dict:
        new_note = note_store.create(NoteCreate(title=title, content=content))
        return {
            "status": "success",
            "message": "Note created successfully",
            "note": new_note.model_dump(mode="json"),
        }

    def _tool_list_notes(self) -> dict:
        notes = note_store.get_all()
        return {
            "status": "success",
            "count": len(notes),
            "notes": [n.model_dump(mode="json") for n in notes],
        }

    def _tool_search_notes(self, query: str) -> dict:
        matches = note_store.search(query)
        return {
            "status": "success",
            "query": query,
            "count": len(matches),
            "results": [n.model_dump(mode="json") for n in matches],
        }

    def run(self, user_message: str) -> str:
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message},
        ]

        # Step 1: Request model completion with tool specs
        response = self.client.chat.completions.create(
            model=settings.model_name,
            messages=messages,
            tools=NOTE_TOOLS,
            tool_choice="auto",
            temperature=0.2,
        )

        response_message = response.choices[0].message
        tool_calls = response_message.tool_calls

        # Step 2: Direct return if no tool was invoked
        if not tool_calls:
            return response_message.content or ""

        # Step 3: Append the assistant's decision to call tools into context
        messages.append(response_message)

        # Step 4: Execute each invoked tool and append the output
        for tool_call in tool_calls:
            func_name = tool_call.function.name
            args = json.loads(tool_call.function.arguments)

            handler = self.tools_dispatcher.get(func_name)
            if handler:
                result = handler(**args)
            else:
                result = {"status": "error", "error": f"Unknown tool: {func_name}"}

            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "name": func_name,
                "content": json.dumps(result, ensure_ascii=False),
            })

        # Step 5: Second call so the LLM synthesizes the tool results into a friendly reply
        final_response = self.client.chat.completions.create(
            model=settings.model_name,
            messages=messages,
            temperature=0.3,
        )

        return final_response.choices[0].message.content or ""


# Singleton instance
agent = NoteAgent()
