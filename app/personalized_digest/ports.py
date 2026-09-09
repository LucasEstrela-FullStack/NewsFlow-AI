"""Dependencies required to generate a personalized daily digest."""

from typing import Protocol

from app.aggregator import UserProfile
from app.news import NewsArticle
from app.pipeline import CollectionBatch

__all__ = ["ArticleCollector", "ArticleRanker", "DigestCreator"]


class ArticleCollector(Protocol):
    """Collect normalized content for a digest run."""

    def collect(self) -> CollectionBatch: ...


class ArticleRanker(Protocol):
    """Order articles according to a user profile."""

    def rank(
        self,
        articles: list[NewsArticle],
        profile: UserProfile,
    ) -> list[NewsArticle]: ...


class DigestCreator(Protocol):
    """Create a Markdown document from normalized articles."""

    def create(self, articles: list[NewsArticle]) -> str: ...
