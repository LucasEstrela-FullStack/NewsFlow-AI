"""Article aggregation use case."""

from app.aggregator.models import UserProfile
from app.news import NewsArticle

__all__ = ["ArticleAggregator"]


class ArticleAggregator:
    """Order articles by their relevance to a user profile."""

    def rank(
        self,
        articles: list[NewsArticle],
        profile: UserProfile,
    ) -> list[NewsArticle]:
        """Return articles ordered from most to least relevant."""
        interests = tuple(interest.lower() for interest in profile.interests)

        return sorted(
            articles,
            key=lambda article: self._relevance_score(article, interests),
            reverse=True,
        )

    @staticmethod
    def _relevance_score(article: NewsArticle, interests: tuple[str, ...]) -> int:
        searchable_content = " ".join(
            value
            for value in (article.title, article.description, article.category)
            if value
        ).lower()

        return sum(interest in searchable_content for interest in interests)
