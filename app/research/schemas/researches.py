# researches.py (schemas)
from pydantic import BaseModel
from typing import List
from ..schemas.users import ShortUserInfoSchema


class ResearchBaseSchema(BaseModel):
    title: str
    body: str


class ResearchSchema(ResearchBaseSchema):
    user_id: int  # The user_id is included in the request to associate the research with a user

    class Config:
        orm_mode = True


class ShortResearchInfoSchema(BaseModel):
    id: int
    title: str

    class Config:
        orm_mode = True


class ResearchInfoSchema(BaseModel):
    id: int
    title: str
    body: str
    creator: ShortUserInfoSchema  # Use the ShortUserInfoSchema to return user info

    class Config:
        orm_mode = True
