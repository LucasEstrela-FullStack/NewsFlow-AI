"""Behavior tests for article persistence."""

from datetime import datetime, timezone

from app.article_persistence import ArticlePersistenceService
from app.news import NewsArticle


class InMemoryArticleRepository:
    """Database boundary substitute used by the use-case test."""

    def __init__(self) -> None:
        self.article_ids: set[str] = set()

    def save(self, articles: list[NewsArticle]) -> int:
        new_article_ids = {article.article_id for article in articles} - self.article_ids
        self.article_ids.update(new_article_ids)
        return len(new_article_ids)


def test_persist_stores_only_articles_that_are_new() -> None:
    repository = InMemoryArticleRepository()
    service = ArticlePersistenceService(repository)
    article = NewsArticle(
        article_id="openai-1",
        title="OpenAI news",
        url="https://example.com/openai-news",
        description="Article description",
        category="research",
        published_at=datetime(2026, 9, 9, tzinfo=timezone.utc),
        source="OpenAI",
    )

    first_result = service.persist([article])
    second_result = service.persist([article])

    assert first_result == 1
    assert second_result == 0
