from fastapi.testclient import TestClient
from src.db.main import get_session
from unittest.mock import Mock
from src import app
import pytest


mock_session = Mock()
mock_user_service = Mock()

def get_mock_session():
    yield mock_session

#override get_session dependency with mock session
app.dependency_overrides[get_session] = get_mock_session    


@pytest.fixture
def fake_session():
    return mock_session



@pytest.fixture
def fake_user_service():
    return mock_user_service


#create a test client obj to return our app 
@pytest.fixture
def test_client():
    return TestClient(app)



