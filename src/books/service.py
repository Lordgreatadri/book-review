from sqlmodel.ext.asyncio.session import AsyncSession
from .schemas import BookCreateModel, BookUpdateModel
from datetime import datetime
from sqlmodel import desc, select
from .models import Book


class BookService:
    async def get_all_books(self, session:AsyncSession):
        statement = select(Book).order_by(desc(Book.created_at))
        result = await session.execute(statement)
        return result.scalars().all()
    
    async def get_book(self, book_uid:str, session: AsyncSession):
        statement = select(Book).where(Book.uid == book_uid)
        result = await session.execute(statement)
        book = result.scalars().first()
        print(book)
        return book if book is not None else None

    async def create_book(self, book_data: BookCreateModel, session: AsyncSession): 
        book_data_dict = book_data.model_dump()
        book = Book(**book_data_dict)
        book.publication_date = datetime.strptime(book_data_dict['publication_date'], "%Y-%m-%d")
        
        session.add(book)
        await session.commit()
        return book


    async def update_book(self, book_uid: str, update_data: BookUpdateModel, session: AsyncSession):
        book_to_update = await self.get_book(book_uid, session)
        if not book_to_update:
            return None
        
        update_data_dict = update_data.model_dump()

        for key, value in update_data_dict.items():
            setattr(book_to_update, key, value)

        await session.commit()

        return book_to_update     

    async def delete_book(self, book_uid: str, session: AsyncSession):
        book_to_delete = await self.get_book(book_uid, session)
        if not book_to_delete:
            return None
        
        await session.delete(book_to_delete)
        await session.commit()

        return {}