from datetime import datetime
from typing import List
from src.books.schemas import Book
import uuid
from pydantic import BaseModel, Field


class UserModel(BaseModel):
    uid:uuid.UUID
    username: str
    email: str
    phone_number: str
    first_name: str
    last_name: str
    is_verified: bool
    role:str
    created_at: datetime
    updated_at: datetime
    books:List[Book]

class CreateUserModel(BaseModel):
    username: str = Field(min_length=6)
    email: str
    phone_number: str = Field(min_length=10, max_length=16)
    first_name: str
    last_name: str
    password: str = Field(min_length=6)

class UserLoginModel(BaseModel):
    username: str
    password: str    