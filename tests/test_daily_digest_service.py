"""Behavior tests for daily digest generation."""

from collections.abc import Sequence
from datetime import UTC, datetime

from app.daily_digest import DailyDigestService
from app.digest import DigestService
from app.news import NewsArticle
from app.pipeline import CollectionPipeline
from app.youtube.models import YouTubeVideo


class StaticNewsSource:
    """Deterministic news source for daily digest behavior tests."""

    def fetch_recent_articles(self) -> list[NewsArticle]:
        return [
            NewsArticle(
                article_id="gpt-5-system-card",
                title="GPT-5 System Card",
                url="https://openai.com/index/gpt-5-system-card/",
                description="Technical report for the GPT-5 model family.",
                category="Research",
                published_at=datetime(2026, 9, 8, 12, 0, tzinfo=UTC),
                source="OpenAI",
            )
        ]


class EmptyVideoSource:
    """Video source that keeps the collection pipeline deterministic."""

    def collect_recent_videos(self, channel_ids: Sequence[str]) -> list[YouTubeVideo]:
        return []


def test_generate_collects_articles_and_creates_the_daily_digest(article_persister) -> None:
    collection_pipeline = CollectionPipeline(
        news_sources=[StaticNewsSource()],
        video_source=EmptyVideoSource(),
        youtube_channel_ids=[],
        article_persister=article_persister,
    )
    service = DailyDigestService(
        collection_pipeline=collection_pipeline,
        digest_service=DigestService(),
    )

    digest = service.generate()

    assert digest == (
        "# NewFlow AI Digest\n\n"
        "# GPT-5 System Card\n\n"
        "- Source: OpenAI\n"
        "- Category: Research\n"
        "- Published at: 2026-09-08T12:00:00+00:00\n"
        "- Original URL: https://openai.com/index/gpt-5-system-card/\n\n"
        "## Description\n\n"
        "Technical report for the GPT-5 model family."
    )
