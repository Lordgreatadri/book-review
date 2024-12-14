from fastapi.testclient import TestClient
from src.auth.dependencies import AccessTokenBearer, RefereshTokenBearer, RoleChecker
from src.db.main import get_session
from unittest.mock import Mock
from src.db.models import Book
from datetime import datetime
from src import app
import pytest
import uuid



mock_session = Mock()
mock_user_service = Mock()
mock_book_service = Mock()
mock_review_service = Mock()


def get_mock_session():
    yield mock_session


access_token_bearer = AccessTokenBearer()
refresh_token_bearer = RefereshTokenBearer()
role_checker = RoleChecker(['admin'])


#override get_session dependency with mock session
app.dependency_overrides[get_session] = get_mock_session
app.dependency_overrides[role_checker] = Mock()
app.dependency_overrides[refresh_token_bearer]= Mock()





@pytest.fixture
def fake_session():
    return mock_session



@pytest.fixture
def fake_user_service():
    return mock_user_service


@pytest.fixture
def fake_book_service():
    return mock_book_service


@pytest.fixture
def fake_review_service():
    return mock_review_service


@pytest.fixture
def test_book():
    return Book(
        uid=uuid.uuid4(),
        user_uid=uuid.uuid4(),
        title="sample title",
        publishe="Mr. Publisher",
        page_count=200,
        published_date=datetime.now(),
        update_at=datetime.now()
    )


#create a test client obj to return our app 
@pytest.fixture
def test_client():
    return TestClient(app)



