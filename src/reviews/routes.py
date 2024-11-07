from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.models import User
from src.db.main import get_session
from src.auth.dependencies import get_current_user
from .schemas import ReviewModel,CreateReviewModel
from .services import ReviewService
from src.exceptions.errors import (
    NewResourceServerError
) 

review_router = APIRouter()
review_service = ReviewService()


@review_router.post("/books/{book_uid}", response_model=ReviewModel )
async def create_book_review(
    book_uid:str, 
    review_data:CreateReviewModel,
    current_user:User = Depends(get_current_user), 
    session:AsyncSession = Depends(get_session)
):
    email = current_user.email

    review = await review_service.create_reviews(
        email, book_uid, review_data, session
        )

    if not review:
        raise NewResourceServerError()
     
    return review
