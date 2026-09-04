"""Domain models shared by news sources."""

from dataclasses import dataclass
from datetime import datetime

__all__ = ["NewsArticle"]


@dataclass(frozen=True, slots=True)
class NewsArticle:
    """Source-independent article metadata collected from a news feed."""

    article_id: str
    title: str
    url: str
    description: str | None
    category: str | None
    published_at: datetime
    source: str
