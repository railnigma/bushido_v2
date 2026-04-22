from datetime import date, datetime
from enum import Enum

from pydantic import BaseModel, Field, ConfigDict


class TaskStatus(str, Enum):
    NEW = "new"
    IN_PROGRESS = "in_progress"
    DONE = "done"


class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: str | None = None
    task_date: date
    status: TaskStatus = TaskStatus.NEW


class TaskUpdate(BaseModel):
    title: str | None = Field(None, min_length=1, max_length=255)
    description: str | None = None
    task_date: date | None = None
    status: TaskStatus | None = None


class TaskResponse(BaseModel):
    id: int
    title: str
    description: str | None
    task_date: date
    status: TaskStatus
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)