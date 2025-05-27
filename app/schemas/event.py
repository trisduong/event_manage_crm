import uuid
from pydantic import BaseModel, Field
from datetime import datetime
from typing import List


class EventBase(BaseModel):
    slug: str
    title: str
    description: str | None = None
    startAt: datetime
    endAt: datetime
    venue: str | None = None
    maxCapacity: int = Field(default=0, ge=0)
    owner: str | None = None
    hosts: List[str] | None = []


class EventCreate(EventBase):
    pass


class EventOut(EventBase):
    id: str

    class Config:
        orm_mode = True
