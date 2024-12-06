from typing import List
from pydantic import BaseModel
from datetime import datetime


class ResearchBase(BaseModel):
    title: str
    description: str
    cost: float
    duration_in_days: int
    category: str
    is_published: bool


class ResearchCreate(ResearchBase):
    pass


class ResearchUpdate(ResearchBase):
    pass


class ResearchCreateList(BaseModel):
    researches: List[ResearchCreate]


class ResearchResponse(BaseModel):
    id: int
    title: str
    description: str
    cost: float
    duration_in_days: int
    category: str
    is_published: bool
    date_created: datetime
    creator_id: int

    class Config:
        orm_mode = True
