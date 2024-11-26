from typing import List

from pydantic import BaseModel


class ResearchBase(BaseModel):
    title: str
    body: str


class ResearchCreate(ResearchBase):
    pass


class ResearchUpdate(ResearchBase):
    pass


class ResearchCreateList(BaseModel):
    researches: List[ResearchCreate]


class ResearchResponse(BaseModel):
    id: int
    title: str
    body: str
    creator_id: int

    class Config:
        orm_mode = True
