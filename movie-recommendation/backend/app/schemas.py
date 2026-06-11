from typing import Literal

from pydantic import BaseModel


class ChatMessage(BaseModel):
    role: Literal["user", "assistant"]
    content: str


class ChatRequest(BaseModel):
    messages: list[ChatMessage]
    interaction_id: str
    user_id: str = "demo-user"


class ChatResponse(BaseModel):
    message: ChatMessage
