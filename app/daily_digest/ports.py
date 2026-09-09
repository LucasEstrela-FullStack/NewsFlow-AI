"""Dependencies required to generate a daily digest."""

from typing import Protocol

from app.news import NewsArticle
from app.pipeline import CollectionBatch

__all__ = ["ArticleCollector", "DigestCreator"]


class ArticleCollector(Protocol):
    """Collect normalized content for a digest run."""

    def collect(self) -> CollectionBatch: ...


class DigestCreator(Protocol):
    """Create a Markdown document from normalized articles."""

    def create(self, articles: list[NewsArticle]) -> str: ...
