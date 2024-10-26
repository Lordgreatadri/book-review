from pydantic import BaseModel
from datetime import datetime, date
import uuid

class Book(BaseModel):
    uid: uuid.UUID
    title: str
    author: str
    publisher: str
    publication_date: date
    page_count: int
    user_uid:uuid.UUID = None
    created_at: datetime
    updated_at: datetime



class BookResponseModel(BaseModel):
    uid: uuid.UUID
    title: str
    author: str
    publisher: str
    publication_date: date
    page_count: int
    user_uid:uuid.UUID = None
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True  # This allows Pydantic to work with ORM objects like SQLAlchemy or SQLModel

  



class BookCreateModel(BaseModel):
    title: str
    author: str
    publisher: str
    publication_date: str
    page_count: int


class BookUpdateModel(BaseModel):
    title: str
    author: str
    publisher: str
    publication_date: date
    page_count: int
