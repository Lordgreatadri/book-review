from fastapi import APIRouter, status, Depends, Request
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio.session import AsyncSession
from typing import Optional, List
from src.books.schemas import Book, BookDetailsModel, BookUpdateModel, BookCreateModel, BookResponseModel
from src.auth.dependencies import AccessTokenBearer, RoleChecker
from src.db.main import get_session
from .service import BookService
from src.config import Config
from src.exceptions.errors import (
    SpecifiedResourceNotFound,
    NewResourceServerError,
    BookNotFound
) 



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
       raise NewResourceServerError()
    

    return book


@router.get("/{book_uid}", response_model=Optional[BookDetailsModel], dependencies=[role_checker])
async def get_book(
        book_uid: str, 
        session: AsyncSession = Depends(get_session),
        token_details: dict = Depends(access_token_bearer)
    ):
    book = await book_service.get_book(book_uid, session)

    if not book:
        raise BookNotFound()
    
    return book



@router.get("/user/{user_uid}", response_model=List[BookResponseModel], dependencies=[role_checker])
async def get_user_books(
    user_uid: str, 
    session: AsyncSession = Depends(get_session),
    token_details: dict = Depends(access_token_bearer)
) :
    books = await book_service.get_user_books(user_uid,session)

    if not books:
        raise SpecifiedResourceNotFound()
     
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
        raise BookNotFound()
    
    return book


@router.delete("/{book_uid}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[role_checker])
async def delete_book(
        book_uid: str, 
        session: AsyncSession = Depends(get_session),
        token_details: dict = Depends(access_token_bearer)
    ):
    book = await book_service.delete_book(book_uid, session)
    if book is None:
        raise BookNotFound()

    return {"detail": "Book deleted"}

