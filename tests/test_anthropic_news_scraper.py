"""Behavior tests for the Anthropic news scraper."""

from datetime import UTC, datetime

from app.news import NewsArticle
from app.anthropic_news import AnthropicNewsScraper


ANTHROPIC_RSS_FEED = """\
<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
  <channel>
    <title>Anthropic News</title>
    <item>
      <title>Building reliable AI systems</title>
      <description>Practical guidance for production AI systems.</description>
      <link>https://www.anthropic.com/news/reliable-ai-systems</link>
      <guid>https://www.anthropic.com/news/reliable-ai-systems</guid>
      <category>Research</category>
      <pubDate>Sun, 07 Sep 2026 13:15:00 GMT</pubDate>
    </item>
  </channel>
</rss>
"""

OLDER_ANTHROPIC_RSS_FEED = """\
<rss version="2.0">
  <channel>
    <item>
      <title>An older article</title>
      <link>https://www.anthropic.com/news/older-article</link>
      <guid>older-article-id</guid>
      <pubDate>Sat, 05 Sep 2026 13:15:00 GMT</pubDate>
    </item>
  </channel>
</rss>
"""


def test_fetch_recent_articles_maps_anthropic_rss_items() -> None:
    requested_urls: list[str] = []

    def download_feed(url: str) -> str:
        requested_urls.append(url)
        return ANTHROPIC_RSS_FEED

    scraper = AnthropicNewsScraper(
        download_feed=download_feed,
        current_time=lambda: datetime(2026, 9, 8, 12, 0, tzinfo=UTC),
    )

    articles = scraper.fetch_recent_articles()

    assert requested_urls == [
        "https://raw.githubusercontent.com/Olshansk/rss-feeds/main/feeds/feed_anthropic_news.xml",
        "https://raw.githubusercontent.com/Olshansk/rss-feeds/main/feeds/feed_anthropic_research.xml",
        "https://raw.githubusercontent.com/Olshansk/rss-feeds/main/feeds/feed_anthropic_engineering.xml",
    ]
    assert articles == [
        NewsArticle(
            article_id="https://www.anthropic.com/news/reliable-ai-systems",
            title="Building reliable AI systems",
            url="https://www.anthropic.com/news/reliable-ai-systems",
            description="Practical guidance for production AI systems.",
            category="Research",
            published_at=datetime(2026, 9, 7, 13, 15, tzinfo=UTC),
            source="Anthropic",
        )
    ]


def test_fetch_recent_articles_deduplicates_across_feeds_and_filters_old_items() -> None:
    scraper = AnthropicNewsScraper(
        download_feed=lambda url: (
            OLDER_ANTHROPIC_RSS_FEED if url.endswith("engineering.xml") else ANTHROPIC_RSS_FEED
        ),
        current_time=lambda: datetime(2026, 9, 8, 12, 0, tzinfo=UTC),
    )

    articles = scraper.fetch_recent_articles()

    assert [article.article_id for article in articles] == [
        "https://www.anthropic.com/news/reliable-ai-systems"
    ]
