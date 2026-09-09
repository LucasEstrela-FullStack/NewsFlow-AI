"""Contract tests for the SQLAlchemy article repository."""

from datetime import datetime, timezone

from sqlalchemy import create_engine

from app.database.articles import SqlAlchemyArticleRepository, create_article_table
from app.news import NewsArticle


def test_save_persists_an_article_once_even_when_received_twice() -> None:
    engine = create_engine("sqlite://")
    create_article_table(engine)
    repository = SqlAlchemyArticleRepository(engine)
    article = NewsArticle(
        article_id="anthropic-1",
        title="Anthropic news",
        url="https://example.com/anthropic-news",
        description=None,
        category=None,
        published_at=datetime(2026, 9, 9, tzinfo=timezone.utc),
        source="Anthropic",
    )

    saved_count = repository.save([article, article])
    repeated_saved_count = SqlAlchemyArticleRepository(engine).save([article])

    assert saved_count == 1
    assert repeated_saved_count == 0
