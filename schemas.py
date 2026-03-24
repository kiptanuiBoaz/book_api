from email.mime import audio

from pydantic import BaseModel


class BookCreate(BaseModel()):
    title: str
    audior: str
    year: int


class BookRead(BaseModel()):
    id: int

    class Config:
        form_attributes = True
