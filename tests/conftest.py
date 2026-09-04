"""Shared test fixtures."""

import pytest
from flask.testing import FlaskClient

from app import create_app
from config import Settings


@pytest.fixture
def client() -> FlaskClient:
    settings = Settings(
        environment="testing",
        debug=False,
        secret_key="test-secret",
    )
    application = create_app(settings)
    application.config.update(TESTING=True)

    return application.test_client()
