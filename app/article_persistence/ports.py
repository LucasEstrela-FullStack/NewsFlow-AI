"""Ports owned by the article persistence use case."""

from typing import Protocol

from app.news import NewsArticle

__all__ = ["ArticleRepository"]


class ArticleRepository(Protocol):
    """Stores source-independent news articles."""

    def save(self, articles: list[NewsArticle]) -> int:
        """Save new articles and return the number of inserted records."""
