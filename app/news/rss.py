"""Shared RSS collection behavior for news sources."""

from collections.abc import Callable, Iterable, Sequence
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from email.utils import parsedate_to_datetime
from xml.etree import ElementTree

from app.news.models import NewsArticle

__all__ = ["RssArticleCollector", "RssFeedError", "RssNewsSource"]


class RssFeedError(RuntimeError):
    """Raised when an RSS feed cannot be collected or interpreted."""


@dataclass(frozen=True, slots=True)
class RssNewsSource:
    """Configuration for a source that publishes news through RSS."""

    feed_url: str
    name: str


class RssArticleCollector:
    """Collect recent article metadata from an RSS source."""

    def __init__(
        self,
        download_feed: Callable[[str], str],
        current_time: Callable[[], datetime],
        lookback: timedelta,
    ) -> None:
        if lookback <= timedelta(0):
            raise ValueError("lookback must be greater than zero")

        self._download_feed = download_feed
        self._current_time = current_time
        self._lookback = lookback

    def collect_recent_articles(
        self,
        sources: Sequence[RssNewsSource],
    ) -> list[NewsArticle]:
        try:
            articles = [
                article
                for source in sources
                for article in self._collect_source_articles(source)
            ]
            return _unique_articles(
                article for article in articles if article.published_at >= self._cutoff_time()
            )
        except (OSError, UnicodeError, ElementTree.ParseError, TypeError, ValueError) as error:
            raise RssFeedError("Unable to collect RSS news feeds") from error

    def _collect_source_articles(self, source: RssNewsSource) -> list[NewsArticle]:
        feed_content = self._download_feed(source.feed_url)
        root = ElementTree.fromstring(feed_content)
        return [
            _map_item(item, source.name)
            for item in root.findall("./channel/item")
        ]

    def _cutoff_time(self) -> datetime:
        current_time = self._current_time()
        if current_time.tzinfo is None:
            raise ValueError("current_time must include a timezone")

        return current_time.astimezone(UTC) - self._lookback


def _map_item(item: ElementTree.Element, source_name: str) -> NewsArticle:
    return NewsArticle(
        article_id=_required_text(item, "guid"),
        title=_required_text(item, "title"),
        url=_required_text(item, "link"),
        description=_optional_text(item, "description"),
        category=_optional_text(item, "category"),
        published_at=_published_at(item),
        source=source_name,
    )


def _unique_articles(articles: Iterable[NewsArticle]) -> list[NewsArticle]:
    unique_articles: list[NewsArticle] = []
    seen_article_ids: set[str] = set()

    for article in articles:
        if article.article_id in seen_article_ids:
            continue

        seen_article_ids.add(article.article_id)
        unique_articles.append(article)

    return unique_articles


def _required_text(item: ElementTree.Element, tag: str) -> str:
    value = _optional_text(item, tag)
    if value is None:
        raise ValueError(f"Missing required feed field: {tag}")

    return value


def _optional_text(item: ElementTree.Element, tag: str) -> str | None:
    element = item.find(tag)
    if element is None or not element.text or not element.text.strip():
        return None

    return element.text.strip()


def _published_at(item: ElementTree.Element) -> datetime:
    value = _required_text(item, "pubDate")
    published_at = parsedate_to_datetime(value)

    if published_at.tzinfo is None:
        raise ValueError("Publication timestamp must include a timezone")

    return published_at.astimezone(UTC)
