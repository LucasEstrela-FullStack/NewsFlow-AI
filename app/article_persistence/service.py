"""Article persistence use case."""

from app.article_persistence.ports import ArticleRepository
from app.news import NewsArticle

__all__ = ["ArticlePersistenceService"]


class ArticlePersistenceService:
    """Persists collected articles through a replaceable repository."""

    def __init__(self, repository: ArticleRepository) -> None:
        self._repository = repository

    def persist(self, articles: list[NewsArticle]) -> int:
        """Store articles that are not already present."""
        return self._repository.save(articles)
