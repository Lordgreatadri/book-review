from fastapi import APIRouter, status, Depends, Request
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio.session import AsyncSession
from typing import Optional, List
from src.books.schemas import Book, BookUpdateModel, BookCreateModel, BookResponseModel
from src.auth.dependencies import AccessTokenBearer, RoleChecker
from src.db.main import get_session
from .service import BookService
from src.config import Config



router = APIRouter()

book_service = BookService()

access_token_bearer = AccessTokenBearer()
role_checker = Depends(RoleChecker(Config.roles))

@router.get('/', response_model=List[BookResponseModel], dependencies=[role_checker])
async def get_books(
    session: AsyncSession = Depends(get_session),
    token_details: dict = Depends(access_token_bearer)
) :
    books = await book_service.get_all_books(session)
    return books



@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Book, dependencies=[role_checker])
async def create_book(
    data : BookCreateModel, 
    session: AsyncSession = Depends(get_session),
    token_details: dict = Depends(access_token_bearer)
) ->dict:
    print(token_details)
    user_uid = token_details['user_uuid']
    # data['user_uid']= user_uid


    book = await book_service.create_book(data, user_uid, session)
    if not book:
       raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="There was an error creating a new book")  

    return book


@router.get("/{book_uid}", response_model=Optional[BookResponseModel], dependencies=[role_checker])
async def get_book(
        book_uid: str, 
        session: AsyncSession = Depends(get_session),
        token_details: dict = Depends(access_token_bearer)
    ):
    book = await book_service.get_book(book_uid, session)

    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The specified book with {book_uid} not found.")
    return book



@router.get("/user/{user_uid}", response_model=List[BookResponseModel], dependencies=[role_checker])
async def get_user_books(
    user_uid: str, 
    session: AsyncSession = Depends(get_session),
    token_details: dict = Depends(access_token_bearer)
) :
    books = await book_service.get_user_books(user_uid,session)

    if not books:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=
        {
            "status_code": status.HTTP_404_NOT_FOUND,
            "message": f"No books found for user with UID: {user_uid}"
        }
        )
    return books



@router.put("/{book_uid}", response_model=BookResponseModel, dependencies=[role_checker])
async def update_book(
        book_uid: str, 
        data: BookUpdateModel, 
        session: AsyncSession = Depends(get_session),
        token_details: dict = Depends(access_token_bearer)
        ):
    book = await book_service.update_book(book_uid, data, session)
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="The specified book not found")

    return book


@router.delete("/{book_uid}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[role_checker])
async def delete_book(
        book_uid: str, 
        session: AsyncSession = Depends(get_session),
        token_details: dict = Depends(access_token_bearer)
    ):
    book = await book_service.delete_book(book_uid, session)
    if book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="The specified book not found")

    return {"detail": "Book deleted"}

