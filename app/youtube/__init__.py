"""Public interface for YouTube video collection."""

from app.youtube.feed import YouTubeAtomFeed, YouTubeFeedError
from app.youtube.models import YouTubeVideo, YouTubeVideoMetadata
from app.youtube.service import YouTubeService
from app.youtube.transcript import YouTubeTranscriptProvider

__all__ = [
    "YouTubeAtomFeed",
    "YouTubeFeedError",
    "YouTubeService",
    "YouTubeTranscriptProvider",
    "YouTubeVideo",
    "YouTubeVideoMetadata",
]
