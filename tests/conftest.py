"""Shared test fixtures."""

import pytest
from flask.testing import FlaskClient

from app import create_app
from app.article_persistence import ArticlePersistenceService
from app.news import NewsArticle
from config import Settings


class InMemoryArticleRepository:
    """Persistence boundary substitute for collection-related tests."""

    def __init__(self) -> None:
        self._article_ids: set[str] = set()

    def save(self, articles: list[NewsArticle]) -> int:
        new_article_ids = {article.article_id for article in articles} - self._article_ids
        self._article_ids.update(new_article_ids)
        return len(new_article_ids)


@pytest.fixture
def article_persister() -> ArticlePersistenceService:
    return ArticlePersistenceService(InMemoryArticleRepository())


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
