import asyncio
from fastapi import FastAPI, HTTPException

from app.config import settings
from app.models import (
    NoteCreate,
    NoteUpdate,
    NoteResponse,
    LLMResponse,
    ChatRequest,
    ChatResponse,
)
from app.services.note_store import note_store
from app.agent.note_agent import agent

app = FastAPI(
    title="Note API & AI Agent",
    version="2.0.0",
    description="A FastAPI service for managing notes with built-in AI Tool-Calling Agent.",
)


@app.get("/")
async def read_root():
    return {
        "message": "Note API & Agent service is running!",
        "version": "2.0.0",
    }


# -------------------------
# Note CRUD Endpoints
# -------------------------

@app.post("/notes", response_model=NoteResponse, status_code=201)
async def create_note(note: NoteCreate):
    return note_store.create(note)


@app.get("/notes", response_model=list[NoteResponse])
async def get_notes():
    return note_store.get_all()


@app.get("/notes/{note_id}", response_model=NoteResponse)
async def get_note(note_id: int):
    note = note_store.get_by_id(note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note


@app.patch("/notes/{note_id}", response_model=NoteResponse)
async def update_note(note_id: int, note_update: NoteUpdate):
    updated = note_store.update(note_id, note_update)
    if not updated:
        raise HTTPException(status_code=404, detail="Note not found")
    return updated


@app.delete("/notes/{note_id}", status_code=204)
async def delete_note(note_id: int):
    success = note_store.delete(note_id)
    if not success:
        raise HTTPException(status_code=404, detail="Note not found")


# -------------------------
# AI Agent Endpoint (Tool Calling)
# -------------------------

@app.post("/agent/chat", response_model=ChatResponse)
async def chat_with_agent(payload: ChatRequest):
    """
    Send natural language instructions to the AI Agent.
    The agent uses Tool Calling to interact with notes automatically.
    """
    reply = agent.run(payload.message)
    return ChatResponse(reply=reply)


# -------------------------
# Utility & Mock Endpoints
# -------------------------

@app.get("/simulate/llm", response_model=LLMResponse)
async def simulate_llm_call(prompt: str):
    await asyncio.sleep(3)
    return LLMResponse(
        prompt=prompt,
        response=f"Mock LLM reply to: {prompt}",
        simulated_latency_seconds=3.0,
    )


@app.get("/config")
async def get_config():
    return {
        "model": settings.model_name,
        "api_key_prefix": settings.openai_api_key[:8] + "..." if settings.openai_api_key else "None",
    }
