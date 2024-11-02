from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi.exceptions import HTTPException
from fastapi import status
from datetime import datetime
from src.db.models import Review
from src.auth.services import UserService
from src.books.service import BookService
from . schemas import CreateReviewModel

user_service = UserService()
book_service = BookService()


class ReviewService:
    async def create_reviews(
            self, 
            user_email:str, 
            book_uid:str,
            review_data: CreateReviewModel,
            session: AsyncSession
        ): 
        try:
            user = await user_service.get_user_by_email(user_email, session)
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, 
                    detail={
                        "status_code": status.HTTP_404_NOT_FOUND,
                        "message": f"User with email {user_email} not found"
                    }
                )
                        
            
            book = await book_service.get_book(book_uid, session)
            if not book:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, 
                    detail={
                        "status_code":status.HTTP_404_NOT_FOUND,
                        "message":f"Book with id {book_uid} not found"
                    }
                )
            
            # review_data_dict = review_data.model_dump()

            review = Review(**review_data.model_dump())
            
            review.user = user
            review.book = book

            session.add(review)
            await session.commit()

            return review
        except Exception as e:
            print(f"Error creating review: {str(e)}")

            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail={
                "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "message": f"An error occurred while creating the review."
            })
   

        
