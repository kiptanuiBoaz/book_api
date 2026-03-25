from email.mime import audio

from pydantic import BaseModel


class BookCreate(BaseModel):
    title: str
    author: str
    year: int


class BookRead(BaseModel):
    id: int
    title: str
    author: str
    year: int

    class Config:
        form_attributes = True
