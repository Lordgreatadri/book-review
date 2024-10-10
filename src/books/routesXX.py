from fastapi import APIRouter, Header, status
from fastapi.exceptions import HTTPException
from typing import Optional, List
from src.books.book_data import books
from src.books.schemas import Book, Book, BookUpdateModel

router = APIRouter()

#[title('Load all books')]
@router.get('/', response_model=List[Book])
async def get_books():
    return books


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_book(data : Book) ->dict:
    book = data.model_dump()
    books.append(book)
    return book


@router.get("/{book_id}", response_model=Optional[Book])
async def get_book(book_id: int):
    book = next((book for book in books if book['id'] == book_id), None)
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="The specified book not found")
    return book


@router.put("/{book_id}", response_model=Book)
async def update_book(book_id: int, data: BookUpdateModel):
    book = next((book for book in books if book['id'] == book_id), None)
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="The specified book not found")
    book.update(data.dict(exclude_unset=True))

    return book


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int):
    book = next((book for book in books if book['id'] == book_id), None)
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="The specified book not found")
    books.remove(book)
    return {"detail": "Book deleted"}


@router.get("/header")
async def get_headers(accept:str = Header(None), content_type:str = Header(None), user_agent:str = Header(None), host:str = Header(None)) :
    request_header = {}

    request_header['Accept'] = accept
    request_header['Content-Type'] = content_type
    request_header['User-Agent'] = user_agent
    request_header['Host'] = host

    return request_header