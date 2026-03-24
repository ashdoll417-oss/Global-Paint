import pytest
import os
from app import create_app, db
from shared.models import Base

@pytest.fixture
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",  # In-memory DB for tests
    })
    yield app
    # Cleanup after test

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()

@pytest.fixture
def init_database(app):
    with app.app_context():
        Base.metadata.create_all(bind=db.engine)
        yield
        Base.metadata.drop_all(bind=db.engine)
