"""Behavior tests for the collection pipeline."""

from collections.abc import Sequence
from datetime import UTC, datetime

from app.news import NewsArticle
from app.pipeline import CollectionBatch, CollectionPipeline
from app.youtube.models import YouTubeVideo


class FakeNewsSource:
    def __init__(self, articles: list[NewsArticle]) -> None:
        self._articles = articles

    def fetch_recent_articles(self) -> list[NewsArticle]:
        return self._articles


class FakeVideoSource:
    def __init__(self, videos: list[YouTubeVideo]) -> None:
        self._videos = videos
        self.channel_ids: Sequence[str] | None = None

    def collect_recent_videos(self, channel_ids: Sequence[str]) -> list[YouTubeVideo]:
        self.channel_ids = channel_ids
        return self._videos


def test_collect_returns_content_from_all_configured_sources() -> None:
    published_at = datetime(2026, 9, 8, 12, 0, tzinfo=UTC)
    openai_article = NewsArticle(
        article_id="openai-article",
        title="OpenAI article",
        url="https://openai.com/news/article",
        description=None,
        category=None,
        published_at=published_at,
        source="OpenAI",
    )
    anthropic_article = NewsArticle(
        article_id="anthropic-article",
        title="Anthropic article",
        url="https://www.anthropic.com/news/article",
        description=None,
        category=None,
        published_at=published_at,
        source="Anthropic",
    )
    youtube_video = YouTubeVideo(
        video_id="video-id",
        title="YouTube video",
        url="https://youtube.com/watch?v=video-id",
        channel_name="AI Channel",
        published_at=published_at,
        transcript="Video transcript",
    )
    video_source = FakeVideoSource([youtube_video])
    pipeline = CollectionPipeline(
        news_sources=[
            FakeNewsSource([openai_article]),
            FakeNewsSource([anthropic_article]),
        ],
        video_source=video_source,
        youtube_channel_ids=["channel-id"],
    )

    batch = pipeline.collect()

    assert batch == CollectionBatch(
        articles=[openai_article, anthropic_article],
        videos=[youtube_video],
    )
    assert video_source.channel_ids == ["channel-id"]
