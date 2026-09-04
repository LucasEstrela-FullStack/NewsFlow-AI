"""Public interface for OpenAI news collection."""

from app.openai_news.scraper import OpenAINewsFeedError, OpenAINewsScraper

__all__ = ["OpenAINewsFeedError", "OpenAINewsScraper"]
