from datetime import datetime
from typing import List
from src.books.schemas import Book
from src.reviews.schemas import ReviewModel
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


class UserBooksModel(UserModel):    
    books:List[Book]
    reviews: List[ReviewModel]

class CreateUserModel(BaseModel):
    username: str = Field(min_length=6)
    email: str
    phone_number: str = Field(min_length=10, max_length=16)
    first_name: str
    last_name: str
    password: str = Field(min_length=6)
    password_confirmation: str = Field(min_length=6)

class UserLoginModel(BaseModel):
    username: str
    password: str    


class EmailModel(BaseModel):
    email_addresses: List[str]



class PasswordResetRequestModel(BaseModel):
    email:str  


class PasswordResetModel(BaseModel):
    new_password:str = Field(min_length=6)
    confirm_password:str = Field(min_length=6)




    
      