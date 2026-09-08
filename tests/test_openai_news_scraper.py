"""Behavior tests for the OpenAI news scraper."""

from datetime import UTC, datetime

import pytest

from app.news import NewsArticle
from app.openai_news import OpenAINewsFeedError, OpenAINewsScraper


OPENAI_RSS_FEED = """\
<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
  <channel>
    <title>OpenAI News</title>
    <item>
      <title>Building reliable AI systems</title>
      <description>Practical techniques for reliable applications.</description>
      <link>https://openai.com/index/reliable-ai-systems</link>
      <guid>https://openai.com/index/reliable-ai-systems</guid>
      <category>Engineering</category>
      <pubDate>Thu, 03 Sep 2026 13:15:00 GMT</pubDate>
    </item>
    <item>
      <title>An older announcement</title>
      <description>This item is outside the collection window.</description>
      <link>https://openai.com/index/older-announcement</link>
      <guid>https://openai.com/index/older-announcement</guid>
      <pubDate>Wed, 02 Sep 2026 10:00:00 GMT</pubDate>
    </item>
  </channel>
</rss>
"""

DUPLICATE_OPENAI_RSS_FEED = """\
<rss version="2.0">
  <channel>
    <item>
      <title>Original article</title>
      <link>https://openai.com/index/same-article</link>
      <guid>same-article-id</guid>
      <pubDate>Thu, 03 Sep 2026 14:00:00 GMT</pubDate>
    </item>
    <item>
      <title>Repeated article</title>
      <link>https://openai.com/index/same-article</link>
      <guid>same-article-id</guid>
      <pubDate>Thu, 03 Sep 2026 14:00:00 GMT</pubDate>
    </item>
  </channel>
</rss>
"""


def test_fetch_recent_articles_maps_openai_rss_items() -> None:
    requested_urls: list[str] = []

    def download_feed(url: str) -> str:
        requested_urls.append(url)
        return OPENAI_RSS_FEED

    scraper = OpenAINewsScraper(
        download_feed=download_feed,
        current_time=lambda: datetime(2026, 9, 4, 12, 0, tzinfo=UTC),
    )

    articles = scraper.fetch_recent_articles()

    assert requested_urls == ["https://openai.com/news/rss.xml"]
    assert articles == [
        NewsArticle(
            article_id="https://openai.com/index/reliable-ai-systems",
            title="Building reliable AI systems",
            url="https://openai.com/index/reliable-ai-systems",
            description="Practical techniques for reliable applications.",
            category="Engineering",
            published_at=datetime(2026, 9, 3, 13, 15, tzinfo=UTC),
            source="OpenAI",
        )
    ]


def test_fetch_recent_articles_removes_duplicate_article_ids() -> None:
    scraper = OpenAINewsScraper(
        download_feed=lambda _: DUPLICATE_OPENAI_RSS_FEED,
        current_time=lambda: datetime(2026, 9, 4, 12, 0, tzinfo=UTC),
    )

    articles = scraper.fetch_recent_articles()

    assert [article.article_id for article in articles] == ["same-article-id"]
    assert articles[0].description is None
    assert articles[0].category is None


def test_fetch_recent_articles_wraps_transport_failures() -> None:
    def unavailable_feed(_: str) -> str:
        raise TimeoutError("OpenAI feed timed out")

    scraper = OpenAINewsScraper(download_feed=unavailable_feed)

    with pytest.raises(OpenAINewsFeedError) as error:
        scraper.fetch_recent_articles()

    assert isinstance(error.value.__cause__, TimeoutError)
