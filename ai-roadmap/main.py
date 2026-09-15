# main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from datetime import datetime

app = FastAPI(title="Note API", version="1.0.0")

# مدل داده
class Note(BaseModel):
    title: str
    content: str

class NoteResponse(Note):
    id: int
    created_at: str

# دیتابیس موقت (فعلاً تو حافظه)
notes: List[NoteResponse] = []
next_id = 1

@app.get("/")
def read_root():
    return {"message": "FastAPI is up and running!"}

@app.post("/notes", response_model=NoteResponse)
def create_note(note: Note):
    global next_id
    new_note = NoteResponse(
        id=next_id,
        title=note.title,
        content=note.content,
        created_at=datetime.now().isoformat()
    )
    notes.append(new_note)
    next_id += 1
    return new_note

@app.get("/notes", response_model=List[NoteResponse])
def get_notes():
    return notes

@app.get("/notes/{note_id}", response_model=NoteResponse)
def get_note(note_id: int):
    for note in notes:
        if note.id == note_id:
            return note
    raise HTTPException(status_code=404, detail="Note not found")
