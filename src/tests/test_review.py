


from src.reviews.schemas import CreateReviewModel


review_prefix =f"/api/v1/reviews"


# test for review creation

def test_create_book_review(
    fake_session, fake_review_service, test_book, test_client
):
    data = {
        "rating": 5,
        "review_text": "Great book!",
    }

    response = test_client.post(f"{review_prefix}/{test_book.uid}")

    review_data= CreateReviewModel(**data)
    
    assert fake_review_service.create_reviews_called_once()
    assert fake_review_service.create_reviews_called_once_with(review_data, fake_session)
    assert response.status_code == 404