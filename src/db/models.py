from typing import List, Optional
from sqlmodel import SQLModel, Field, Column, String, Relationship
import sqlalchemy.dialects.postgresql as pg
from pydantic import BaseModel
from datetime import datetime, date
import uuid





class User(SQLModel, table=True):
    __tablename__ = "users"
    uid:uuid.UUID= Field(
        sa_column=Column(
            pg.UUID,
            primary_key=True,
            nullable=False,
            default= uuid.uuid4,
            unique=True,
            index=True
        )
    )
    username:str
    email:str = Field(sa_column=Column(String, unique=True, nullable=False, index=True))
    phone_number:str = Field(sa_column=Column(String, unique=True, nullable=False,index=True))
    first_name:str
    last_name:str
    password:str = Field(String, exclude=True)
    is_verified:bool=False
    role:str = Field(sa_column=Column(pg.VARCHAR, nullable=False, server_default='user'))
    created_at:datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now()))
    updated_at:datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now()))
    books: List["Book"] = Relationship(back_populates="user", sa_relationship_kwargs={"lazy":"selectin"})
    reviews: List["Review"] = Relationship(back_populates="user", sa_relationship_kwargs={"lazy":"selectin"})

    def __repr__(self):
        return f"<User {self.username}>"
     









class BookTag(SQLModel, table=True):
    book_id: uuid.UUID = Field(default=None, foreign_key="books.uid", primary_key=True)
    tag_id: uuid.UUID = Field(default=None, foreign_key="tags.uid", primary_key=True)


class Tag(SQLModel, table=True):
    __tablename__ = "tags"
    uid: uuid.UUID = Field(
        sa_column=Column(pg.UUID, nullable=False, primary_key=True, default=uuid.uuid4)
    )
    name: str = Field(sa_column=Column(pg.VARCHAR, nullable=False))
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    books: List["Book"] = Relationship(
        link_model=BookTag,
        back_populates="tags",
        sa_relationship_kwargs={"lazy": "selectin"},
    )

    def __repr__(self) -> str:
        return f"<Tag {self.name}>"






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
    user: Optional["User"] = Relationship(back_populates="books")
    reviews: List["Review"] = Relationship(back_populates="book", sa_relationship_kwargs={"lazy":"selectin"})
    tags: List[Tag] = Relationship(
        link_model=BookTag,
        back_populates="books",
        sa_relationship_kwargs={"lazy": "selectin"},
    )
    

    def __repr__(self):
        return f"<Book {self.title}>"


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



class Review(SQLModel, table = True):
    __tablename__ = "reviews"

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
    review_text: str
    rating:int = Field(lt=5) 
    user_uid: Optional[uuid.UUID] = Field(default=None, foreign_key="users.uid", index=True, ondelete="CASCADE")
    book_uid: Optional[uuid.UUID] = Field(default=None, foreign_key="books.uid", index=True, ondelete="CASCADE")
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now()))
    updated_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now()))
    user: Optional[User] = Relationship(back_populates="reviews")
    book: Optional[Book] = Relationship(back_populates="reviews")
    def __repr__(self):
        return f"<Review for book {self.book_uid} by user {self.user_uid}>"




