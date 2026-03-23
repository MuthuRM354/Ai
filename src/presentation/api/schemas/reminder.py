from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class ReminderCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    due_at: Optional[datetime] = None


class ReminderUpdate(BaseModel):
    completed: bool


class ReminderOut(BaseModel):
    id: int
    title: str
    completed: bool
    due_at: Optional[datetime] = None
    created_at: datetime