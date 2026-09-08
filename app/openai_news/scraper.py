"""OpenAI news RSS scraper."""

from collections.abc import Callable, Iterable
from datetime import UTC, datetime, timedelta
from email.utils import parsedate_to_datetime
from xml.etree import ElementTree

from app.http_client import download_text
from app.news import NewsArticle

__all__ = ["OpenAINewsFeedError", "OpenAINewsScraper"]

_OPENAI_NEWS_FEED_URL = "https://openai.com/news/rss.xml"
_SOURCE_NAME = "OpenAI"


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
        if lookback <= timedelta(0):
            raise ValueError("lookback must be greater than zero")

        self._download_feed = download_feed or download_text
        self._current_time = current_time or _utc_now
        self._lookback = lookback

    def fetch_recent_articles(self) -> list[NewsArticle]:
        feed_content = self._fetch_feed()
        cutoff = self._cutoff_time()

        try:
            root = ElementTree.fromstring(feed_content)
            articles = [
                self._map_item(item) for item in root.findall("./channel/item")
            ]
            recent_articles = (
                article for article in articles if article.published_at >= cutoff
            )
            return _unique_articles(recent_articles)
        except (ElementTree.ParseError, TypeError, ValueError) as error:
            raise OpenAINewsFeedError("Invalid OpenAI news feed") from error

    def _fetch_feed(self) -> str:
        try:
            return self._download_feed(_OPENAI_NEWS_FEED_URL)
        except (OSError, UnicodeError) as error:
            raise OpenAINewsFeedError("Unable to download OpenAI news feed") from error

    @staticmethod
    def _map_item(item: ElementTree.Element) -> NewsArticle:
        return NewsArticle(
            article_id=_required_text(item, "guid"),
            title=_required_text(item, "title"),
            url=_required_text(item, "link"),
            description=_optional_text(item, "description"),
            category=_optional_text(item, "category"),
            published_at=_published_at(item),
            source=_SOURCE_NAME,
        )

    def _cutoff_time(self) -> datetime:
        current_time = self._current_time()
        if current_time.tzinfo is None:
            raise ValueError("current_time must include a timezone")

        return current_time.astimezone(UTC) - self._lookback


def _utc_now() -> datetime:
    return datetime.now(UTC)


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
