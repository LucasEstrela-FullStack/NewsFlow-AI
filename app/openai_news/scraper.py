"""OpenAI news RSS scraper."""

from collections.abc import Callable
from datetime import UTC, datetime, timedelta

from app.http_client import download_text
from app.news import NewsArticle
from app.news.rss import RssArticleCollector, RssFeedError, RssNewsSource

__all__ = ["OpenAINewsFeedError", "OpenAINewsScraper"]

_OPENAI_NEWS_SOURCE = RssNewsSource(
    feed_url="https://openai.com/news/rss.xml",
    name="OpenAI",
)


class OpenAINewsFeedError(RuntimeError):
    """Raised when the OpenAI news feed cannot be interpreted."""


class OpenAINewsScraper:
    """Collect article metadata from the official OpenAI news feed."""

    def __init__(
        self,
        download_feed: Callable[[str], str] | None = None,
        current_time: Callable[[], datetime] | None = None,
        lookback: timedelta = timedelta(hours=24),
    ) -> None:
        self._collector = RssArticleCollector(
            download_feed=download_feed or download_text,
            current_time=current_time or _utc_now,
            lookback=lookback,
        )

    def fetch_recent_articles(self) -> list[NewsArticle]:
        try:
            return self._collector.collect_recent_articles((_OPENAI_NEWS_SOURCE,))
        except RssFeedError as error:
            raise OpenAINewsFeedError("Unable to collect OpenAI news") from error.__cause__


def _utc_now() -> datetime:
    return datetime.now(UTC)
