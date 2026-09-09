"""Behavior tests for digest creation."""

from datetime import UTC, datetime

from app.digest import DigestService
from app.news import NewsArticle


def test_create_combines_articles_into_a_markdown_digest() -> None:
    articles = [
        NewsArticle(
            article_id="gpt-5-system-card",
            title="GPT-5 System Card",
            url="https://openai.com/index/gpt-5-system-card/",
            description="Technical report for the GPT-5 model family.",
            category="Research",
            published_at=datetime(2026, 9, 8, 12, 0, tzinfo=UTC),
            source="OpenAI",
        ),
        NewsArticle(
            article_id="claude-code",
            title="Claude Code Updates",
            url="https://www.anthropic.com/news/claude-code",
            description="Updates for the Claude Code product.",
            category="Product",
            published_at=datetime(2026, 9, 7, 15, 30, tzinfo=UTC),
            source="Anthropic",
        ),
    ]

    digest = DigestService().create(articles)

    assert digest == (
        "# NewFlow AI Digest\n\n"
        "# GPT-5 System Card\n\n"
        "- Source: OpenAI\n"
        "- Category: Research\n"
        "- Published at: 2026-09-08T12:00:00+00:00\n"
        "- Original URL: https://openai.com/index/gpt-5-system-card/\n\n"
        "## Description\n\n"
        "Technical report for the GPT-5 model family.\n\n"
        "---\n\n"
        "# Claude Code Updates\n\n"
        "- Source: Anthropic\n"
        "- Category: Product\n"
        "- Published at: 2026-09-07T15:30:00+00:00\n"
        "- Original URL: https://www.anthropic.com/news/claude-code\n\n"
        "## Description\n\n"
        "Updates for the Claude Code product."
    )
