from datetime import datetime

from pydantic import BaseModel


class CreateJokeSchema(BaseModel):
    joke: str


class CreateSpoilerJokeSchema(BaseModel):
    joke: str
    spoiler: str


class CreateMemeSchema(BaseModel):
    link: str


class JokeSchema(BaseModel):
    id: int
    joke: str
    creation_date: datetime

    class Config:
        orm_mode = True


class SpoilerJokeSchema(BaseModel):
    id: int
    joke: str
    spoiler: str
    creation_date: datetime

    class Config:
        orm_mode = True


class MemeSchema(BaseModel):
    id: int
    link: str
    creation_date: datetime

    class Config:
        orm_mode = True
