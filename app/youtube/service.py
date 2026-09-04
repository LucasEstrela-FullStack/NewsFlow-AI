"""Use case for collecting YouTube videos."""

from collections.abc import Sequence

from app.youtube.models import YouTubeVideo, YouTubeVideoMetadata
from app.youtube.ports import TranscriptProvider, VideoFeed

__all__ = ["YouTubeService"]


class YouTubeService:
    """Collect videos from configured channels and enrich their content."""

    def __init__(
        self,
        video_feed: VideoFeed,
        transcript_provider: TranscriptProvider,
    ) -> None:
        self._video_feed = video_feed
        self._transcript_provider = transcript_provider

    def collect_recent_videos(self, channel_ids: Sequence[str]) -> list[YouTubeVideo]:
        videos: list[YouTubeVideo] = []

        for channel_id in channel_ids:
            metadata_entries = self._video_feed.fetch_recent_videos(channel_id)
            videos.extend(self._enrich(entry) for entry in metadata_entries)

        return videos

    def _enrich(self, metadata: YouTubeVideoMetadata) -> YouTubeVideo:
        return YouTubeVideo(
            video_id=metadata.video_id,
            title=metadata.title,
            url=metadata.url,
            channel_name=metadata.channel_name,
            published_at=metadata.published_at,
            transcript=self._transcript_provider.fetch_transcript(metadata.video_id),
        )
