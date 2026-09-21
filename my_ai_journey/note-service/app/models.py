from datetime import datetime
from pydantic import BaseModel, Field


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


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, description="User instruction or question for the agent")


class ChatResponse(BaseModel):
    reply: str
