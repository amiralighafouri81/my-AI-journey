from datetime import datetime, timezone
from app.models import NoteResponse, NoteCreate, NoteUpdate


class InMemoryNoteStore:
    def __init__(self):
        self._notes: list[NoteResponse] = []
        self._next_id: int = 1

    @staticmethod
    def _get_current_time() -> datetime:
        return datetime.now(timezone.utc)

    def create(self, note_data: NoteCreate) -> NoteResponse:
        current_time = self._get_current_time()
        new_note = NoteResponse(
            id=self._next_id,
            title=note_data.title,
            content=note_data.content,
            created_at=current_time,
            updated_at=current_time,
        )
        self._notes.append(new_note)
        self._next_id += 1
        return new_note

    def get_all(self) -> list[NoteResponse]:
        return self._notes

    def get_by_id(self, note_id: int) -> NoteResponse | None:
        for note in self._notes:
            if note.id == note_id:
                return note
        return None

    def update(self, note_id: int, note_update: NoteUpdate) -> NoteResponse | None:
        for index, note in enumerate(self._notes):
            if note.id == note_id:
                update_data = note_update.model_dump(exclude_unset=True)
                updated_note = note.model_copy(
                    update={
                        **update_data,
                        "updated_at": self._get_current_time(),
                    }
                )
                self._notes[index] = updated_note
                return updated_note
        return None

    def delete(self, note_id: int) -> bool:
        for index, note in enumerate(self._notes):
            if note.id == note_id:
                self._notes.pop(index)
                return True
        return False

    def search(self, query: str) -> list[NoteResponse]:
        q = query.lower()
        return [
            note for note in self._notes
            if q in note.title.lower() or q in note.content.lower()
        ]


# Singleton instance across the service
note_store = InMemoryNoteStore()
