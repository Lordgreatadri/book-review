from typing import Optional
from pydantic import BaseModel
from sqlmodel import SQLModel, Field, Column, Relationship
from datetime import date, datetime
import sqlalchemy.dialects.postgresql as pg
from src.auth import models
import uuid

class Book(SQLModel, table = True):
    __tablename__ = "books"

    uid: uuid.UUID = Field(
        sa_column=Column(
            pg.UUID,
            primary_key=True,
            nullable=False,
            default= uuid.uuid4,
            unique=True,
            index=True
        )
    )
    title: str
    author: str
    publisher: str
    published:bool = Field(sa_column=Column( server_default='TRUE', nullable=False))
    publication_date: date
    page_count: int
    user_uid: Optional[uuid.UUID] = Field(default=None, foreign_key="users.uid", index=True, ondelete="CASCADE")
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now()))
    updated_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now()))
    user: Optional["models.User"] = Relationship(back_populates="books")
    def __repr__(self):
        return f"<Book {self}>"


class BookResponseModel(BaseModel):
    uid: uuid.UUID
    title: str
    author: str
    publisher: str
    publication_date: date
    page_count: int
    user_uid: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True  # This allows Pydantic to work with ORM objects like SQLAlchemy or SQLModel


class BookUpdateModel(SQLModel):
    title: str
    author: str
    publisher: str
    publication_date: str
    page_count: int
