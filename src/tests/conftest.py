import pytest

from unittest.mock import Mock
from fastapi.testclient import TestClient

from src import app
from src.db.main import get_session
from src.auth.dependencies import RoleChecker, AccessTokenBearer, RefereshTokenRequired

mock_session = Mock()
mock_user_service = Mock()
mock_book_service = Mock()


def get_mock_session():
    yield mock_session


access_token_bearer = AccessTokenBearer()
refresh_token_bearer = RefereshTokenRequired()
role_checker = RoleChecker(['admin'])

app.dependency_overrides[get_session] = get_mock_session
app.dependency_overrides[role_checker] = Mock()
app.dependency_overrides[refresh_token_bearer] = Mock()


# A fixture is a reusable function that provides setup and teardown logic for your tests.
# Instead of repeating setup code in every test (like creating the TestClient, connecting to a DB, etc.),
# You define it once as a fixture — and pytest automatically provides it to any test function that asks for it.
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
def test_client():
    # It simulates a real HTTP client — allowing you to send GET, POST, PUT, etc. requests directly to your FastAPI app, without starting a real server.
    # It behaves like a real browser or API client, but it runs in memory — fast, isolated, and ideal for automated tests.
    return TestClient(app)
