import asyncio
from datetime import datetime, timezone

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from config import settings

app = FastAPI(
    title="Note API",
    version="1.1.0",
    description="A simple FastAPI service for managing notes.",
)


# -------------------------
# Data models
# -------------------------

class NoteCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    content: str = Field(..., min_length=1)


class NoteUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=100)
    content: str | None = Field(default=None, min_length=1)


class NoteResponse(BaseModel):
    id: int
    title: str
    content: str
    created_at: datetime
    updated_at: datetime


class LLMResponse(BaseModel):
    prompt: str
    response: str
    simulated_latency_seconds: float


# -------------------------
# Temporary in-memory storage
# -------------------------

notes: list[NoteResponse] = []
next_id = 1


def get_current_time() -> datetime:
    return datetime.now(timezone.utc)


# -------------------------
# Basic endpoints
# -------------------------

@app.get("/")
async def read_root():
    return {
        "message": "FastAPI is up and running!",
        "service": "Note API",
        "version": "1.1.0",
    }


@app.post(
    "/notes",
    response_model=NoteResponse,
    status_code=201,
)
async def create_note(note: NoteCreate):
    global next_id

    current_time = get_current_time()

    new_note = NoteResponse(
        id=next_id,
        title=note.title,
        content=note.content,
        created_at=current_time,
        updated_at=current_time,
    )

    notes.append(new_note)
    next_id += 1

    return new_note


@app.get(
    "/notes",
    response_model=list[NoteResponse],
)
async def get_notes():
    return notes


@app.get(
    "/notes/{note_id}",
    response_model=NoteResponse,
)
async def get_note(note_id: int):
    for note in notes:
        if note.id == note_id:
            return note

    raise HTTPException(
        status_code=404,
        detail="Note not found",
    )


@app.patch(
    "/notes/{note_id}",
    response_model=NoteResponse,
)
async def update_note(note_id: int, note_update: NoteUpdate):
    for index, note in enumerate(notes):
        if note.id == note_id:
            update_data = note_update.model_dump(exclude_unset=True)

            updated_note = note.model_copy(
                update={
                    **update_data,
                    "updated_at": get_current_time(),
                }
            )

            notes[index] = updated_note
            return updated_note

    raise HTTPException(
        status_code=404,
        detail="Note not found",
    )


@app.delete(
    "/notes/{note_id}",
    status_code=204,
)
async def delete_note(note_id: int):
    for index, note in enumerate(notes):
        if note.id == note_id:
            notes.pop(index)
            return

    raise HTTPException(
        status_code=404,
        detail="Note not found",
    )


# -------------------------
# Mock LLM endpoint
# -------------------------

@app.get(
    "/simulate/llm",
    response_model=LLMResponse,
)
async def simulate_llm_call(prompt: str):
    """
    Simulate a slow network call to an LLM API.
    This endpoint does not call a real language model.
    """
    await asyncio.sleep(3)

    return LLMResponse(
        prompt=prompt,
        response=f"Mock LLM reply to: {prompt}",
        simulated_latency_seconds=3.0,
    )


# -------------------------
# Config endpoint
# -------------------------

@app.get("/config")
async def get_config():
    return {
        "model": settings.model_name,
        "api_key_prefix": settings.openai_api_key[:8] + "...",
    }


# -------------------------
# Error handling demo
# -------------------------

@app.get("/error-demo/{code}")
async def error_demo(code: int):
    if code == 400:
        raise HTTPException(status_code=400, detail="Bad request demo")
    elif code == 401:
        raise HTTPException(status_code=401, detail="Unauthorized demo")
    elif code == 429:
        raise HTTPException(status_code=429, detail="Too many requests demo")
    elif code == 503:
        raise HTTPException(status_code=503, detail="Service unavailable demo")

    return {"message": f"Code {code} is OK"}
