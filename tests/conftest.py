import pytest
from jembe_io_examples import create_app


@pytest.fixture
def app():
    app = create_app({"TESTING": True})
    yield app

@pytest.fixture
def client(app):
    yield app.test_client()