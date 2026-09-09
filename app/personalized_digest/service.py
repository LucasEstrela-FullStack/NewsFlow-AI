"""Personalized daily digest generation use case."""

from app.aggregator import UserProfile
from app.personalized_digest.ports import ArticleCollector, ArticleRanker, DigestCreator

__all__ = ["PersonalizedDailyDigestService"]


class PersonalizedDailyDigestService:
    """Create a daily Markdown digest ordered for a user profile."""

    def __init__(
        self,
        collection_pipeline: ArticleCollector,
        article_aggregator: ArticleRanker,
        digest_service: DigestCreator,
    ) -> None:
        self._collection_pipeline = collection_pipeline
        self._article_aggregator = article_aggregator
        self._digest_service = digest_service

    def generate(self, profile: UserProfile) -> str:
        """Collect, prioritize, and render articles for the supplied profile."""
        collection_batch = self._collection_pipeline.collect()
        ranked_articles = self._article_aggregator.rank(
            collection_batch.articles,
            profile,
        )

        return self._digest_service.create(ranked_articles)
