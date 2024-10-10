from fastapi import APIRouter, status, Depends, Request
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio.session import AsyncSession
from typing import Optional, List
from src.books.schemas import Book, BookUpdateModel, BookCreateModel, BookResponseModel
from src.db.main import get_session
from .service import BookService

router = APIRouter()

book_service = BookService()


@router.get('/', response_model=List[BookResponseModel])
async def get_books(session: AsyncSession = Depends(get_session)) :
    books = await book_service.get_all_books(session)
    return books



@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Book)
async def create_book(data : BookCreateModel, session: AsyncSession = Depends(get_session)) ->dict:
    book = await book_service.create_book(data, session)
    if not book:
       raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="There was an error creating a new book")  

    return book


@router.get("/{book_uid}", response_model=Optional[BookResponseModel])
async def get_book(book_uid: str, session: AsyncSession = Depends(get_session)):
    book = await book_service.get_book(book_uid, session)

    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="The specified book not found")
    return book


@router.put("/{book_uid}", response_model=BookResponseModel)
async def update_book(book_uid: str, data: BookUpdateModel, session: AsyncSession = Depends(get_session)):
    book = await book_service.update_book(book_uid, data, session)
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="The specified book not found")

    return book


@router.delete("/{book_uid}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_uid: str, session: AsyncSession = Depends(get_session)):
    book = await book_service.delete_book(book_uid, session)
    if book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="The specified book not found")

    return {"detail": "Book deleted"}

