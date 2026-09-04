"""Domain models for YouTube content."""

from dataclasses import dataclass
from datetime import datetime

__all__ = ["YouTubeVideo", "YouTubeVideoMetadata"]


@dataclass(frozen=True, slots=True)
class YouTubeVideoMetadata:
    """Video data available from a YouTube channel feed."""

    video_id: str
    title: str
    url: str
    channel_name: str
    published_at: datetime


@dataclass(frozen=True, slots=True)
class YouTubeVideo:
    """A YouTube video enriched with its available transcript."""

    video_id: str
    title: str
    url: str
    channel_name: str
    published_at: datetime
    transcript: str | None
