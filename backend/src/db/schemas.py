from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from .models import Role


class ChatItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    name: str | None = None
    updated_at: datetime


class StepItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    title: str
    url: str
    step_number: int | None = None
    message_id: int


class MessageOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    chat_id: UUID
    role: Role
    content: str
    steps: list[StepItem]
