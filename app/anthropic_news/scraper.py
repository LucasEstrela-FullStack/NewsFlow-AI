"""Anthropic news RSS scraper."""

from collections.abc import Callable
from datetime import UTC, datetime, timedelta

from app.http_client import download_text
from app.news import NewsArticle
from app.news.rss import RssArticleCollector, RssFeedError, RssNewsSource

__all__ = ["AnthropicNewsFeedError", "AnthropicNewsScraper"]

_ANTHROPIC_NEWS_SOURCES = (
    RssNewsSource(
        feed_url="https://raw.githubusercontent.com/Olshansk/rss-feeds/main/feeds/feed_anthropic_news.xml",
        name="Anthropic",
    ),
    RssNewsSource(
        feed_url="https://raw.githubusercontent.com/Olshansk/rss-feeds/main/feeds/feed_anthropic_research.xml",
        name="Anthropic",
    ),
    RssNewsSource(
        feed_url="https://raw.githubusercontent.com/Olshansk/rss-feeds/main/feeds/feed_anthropic_engineering.xml",
        name="Anthropic",
    ),
)


class AnthropicNewsFeedError(RuntimeError):
    """Raised when the Anthropic news feed cannot be interpreted."""


class AnthropicNewsScraper:
    """Collect article metadata from the Anthropic RSS feeds."""

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
            return self._collector.collect_recent_articles(_ANTHROPIC_NEWS_SOURCES)
        except RssFeedError as error:
            raise AnthropicNewsFeedError("Unable to collect Anthropic news") from error.__cause__


def _utc_now() -> datetime:
    return datetime.now(UTC)
