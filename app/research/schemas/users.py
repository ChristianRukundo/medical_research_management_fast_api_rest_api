from pydantic import BaseModel
from typing import List


class UserSchema(BaseModel):
    name: str
    email: str
    password: str


class ShortUserInfoSchema(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class ShortResearchInfoSchema(BaseModel):
    id: int
    title: str

    class Config:
        orm_mode = True


class UserInfoSchema(BaseModel):
    name: str
    id: int
    email: str
    researches: List[ShortResearchInfoSchema] = []  # List of researches associated with the user

    class Config:
        orm_mode = True
