from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime, date
import uuid




class ReviewModel(BaseModel):

    uid: uuid.UUID 
    review_text: str
    rating:int 
    user_uid: Optional[uuid.UUID]
    book_uid: uuid.UUID = None
    created_at: datetime 
    updated_at: datetime

    class Config:
        orm_mode = True


class CreateReviewModel(BaseModel):
    review_text: str
    rating:int  = Field(lte=5)


   