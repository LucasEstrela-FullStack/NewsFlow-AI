"""Application-owned boundaries for YouTube providers."""

from collections.abc import Sequence
from typing import Protocol

from app.youtube.models import YouTubeVideoMetadata

__all__ = ["TranscriptProvider", "VideoFeed"]


class VideoFeed(Protocol):
    """Provides recent metadata for a YouTube channel."""

    def fetch_recent_videos(
        self,
        channel_id: str,
    ) -> Sequence[YouTubeVideoMetadata]: ...


class TranscriptProvider(Protocol):
    """Provides a plain-text transcript when one is available."""

    def fetch_transcript(self, video_id: str) -> str | None: ...
