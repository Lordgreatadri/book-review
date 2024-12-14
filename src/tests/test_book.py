
from src.books.schemas import BookCreateModel, BookDetailsModel

book_prefix =f"/api/v1/books"


# test for book creation
def test_create_book(fake_session, fake_book_service, test_client):
    data = {
        "title": "The Great Gatsby",
        "author": "F. Scott Fitzgerald",
        "publisher":"Mr. Scott",
        "publication_date": "2024-07-30",
        "page_count": 1200,
    }

    response = test_client.post(f"{book_prefix}/", json=data)
    book_create_data = BookCreateModel(**data)
    assert fake_book_service.create_book_called_once()
    assert fake_book_service.create_book_called_once_with(book_create_data, fake_session)


def test_get_all_books(fake_session, fake_book_service, test_client):
    response = test_client.get(f"{book_prefix}/books")

    # assert fake_book_service.get_all_books_called_once()
    assert fake_book_service.get_all_books_called_once_with(fake_session)



def test_get_book_by_uid(test_client, fake_book_service,test_book, fake_session):
    response = test_client.get(f"{book_prefix}/{test_book.uid}")

    assert fake_book_service.get_book_called_once()
    assert fake_book_service.get_book_called_once_with(test_book.uid,fake_session)


def test_update_book_by_uid(test_client, fake_book_service,test_book, fake_session):
    response = test_client.put(f"{book_prefix}/{test_book.uid}")

    assert fake_book_service.get_book_called_once()
    assert fake_book_service.get_book_called_once_with(test_book.uid,fake_session)
