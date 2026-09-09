"""Behavior tests for article aggregation."""

from datetime import UTC, datetime

from app.aggregator import ArticleAggregator, UserProfile
from app.news import NewsArticle


def test_rank_prioritizes_articles_matching_the_user_interests() -> None:
    profile = UserProfile(interests=("research", "agents"))
    articles = [
        NewsArticle(
            article_id="business-update",
            title="Company business update",
            url="https://example.com/business-update",
            description="Financial results for the quarter.",
            category="Company",
            published_at=datetime(2026, 9, 9, tzinfo=UTC),
            source="OpenAI",
        ),
        NewsArticle(
            article_id="agent-research",
            title="Research on reliable agents",
            url="https://example.com/agent-research",
            description="A new research report about AI agents.",
            category="Research",
            published_at=datetime(2026, 9, 9, tzinfo=UTC),
            source="Anthropic",
        ),
    ]

    ranked_articles = ArticleAggregator().rank(articles, profile)

    assert [article.article_id for article in ranked_articles] == [
        "agent-research",
        "business-update",
    ]


def test_rank_preserves_source_order_when_articles_have_equal_relevance() -> None:
    profile = UserProfile(interests=("research",))
    articles = [
        NewsArticle(
            article_id="first-research",
            title="First research update",
            url="https://example.com/first-research",
            description=None,
            category=None,
            published_at=datetime(2026, 9, 9, tzinfo=UTC),
            source="OpenAI",
        ),
        NewsArticle(
            article_id="second-research",
            title="Second research update",
            url="https://example.com/second-research",
            description=None,
            category=None,
            published_at=datetime(2026, 9, 9, tzinfo=UTC),
            source="Anthropic",
        ),
    ]

    ranked_articles = ArticleAggregator().rank(articles, profile)

    assert [article.article_id for article in ranked_articles] == [
        "first-research",
        "second-research",
    ]
