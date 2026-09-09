"""Daily digest generation use case."""

from app.daily_digest.ports import ArticleCollector, DigestCreator

__all__ = ["DailyDigestService"]


class DailyDigestService:
    """Collect articles and create their daily Markdown digest."""

    def __init__(
        self,
        collection_pipeline: ArticleCollector,
        digest_service: DigestCreator,
    ) -> None:
        self._collection_pipeline = collection_pipeline
        self._digest_service = digest_service

    def generate(self) -> str:
        """Collect current articles and return their Markdown digest."""
        collection_batch = self._collection_pipeline.collect()

        return self._digest_service.create(collection_batch.articles)
