"""Behavior tests for article Markdown processing."""

from datetime import UTC, datetime

from app.news import ArticleMarkdownProcessor, NewsArticle


def test_to_markdown_formats_article_metadata_and_description() -> None:
    article = NewsArticle(
        article_id="gpt-5-system-card",
        title="GPT-5 System Card",
        url="https://openai.com/index/gpt-5-system-card/",
        description="Technical report for the GPT-5 model family.",
        category="Research",
        published_at=datetime(2026, 9, 8, 12, 0, tzinfo=UTC),
        source="OpenAI",
    )

    markdown = ArticleMarkdownProcessor().to_markdown(article)

    assert markdown == (
        "# GPT-5 System Card\n\n"
        "- Source: OpenAI\n"
        "- Category: Research\n"
        "- Published at: 2026-09-08T12:00:00+00:00\n"
        "- Original URL: https://openai.com/index/gpt-5-system-card/\n\n"
        "## Description\n\n"
        "Technical report for the GPT-5 model family."
    )
