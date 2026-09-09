"""Use case for collecting content from configured sources."""

from collections.abc import Sequence
from dataclasses import dataclass
from typing import Protocol

from app.news import NewsArticle
from app.youtube.models import YouTubeVideo

__all__ = ["CollectionBatch", "CollectionPipeline"]


class NewsSource(Protocol):
    """Source capable of collecting recent news articles."""

    def fetch_recent_articles(self) -> list[NewsArticle]: ...


class VideoSource(Protocol):
    """Source capable of collecting recent videos from channels."""

    def collect_recent_videos(self, channel_ids: Sequence[str]) -> list[YouTubeVideo]: ...


class ArticlePersister(Protocol):
    """Use case capable of persisting collected articles."""

    def persist(self, articles: list[NewsArticle]) -> int: ...


@dataclass(frozen=True, slots=True)
class CollectionBatch:
    """Content collected during one pipeline execution."""

    articles: list[NewsArticle]
    videos: list[YouTubeVideo]


class CollectionPipeline:
    """Orchestrate content collection without knowing source details."""

    def __init__(
        self,
        news_sources: Sequence[NewsSource],
        video_source: VideoSource,
        youtube_channel_ids: Sequence[str],
        article_persister: ArticlePersister,
    ) -> None:
        self._news_sources = news_sources
        self._video_source = video_source
        self._youtube_channel_ids = youtube_channel_ids
        self._article_persister = article_persister

    def collect(self) -> CollectionBatch:
        articles = [
            article
            for source in self._news_sources
            for article in source.fetch_recent_articles()
        ]
        self._article_persister.persist(articles)
        videos = self._video_source.collect_recent_videos(self._youtube_channel_ids)

        return CollectionBatch(articles=articles, videos=videos)
