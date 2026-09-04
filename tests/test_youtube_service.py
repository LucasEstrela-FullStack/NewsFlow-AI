"""Behavior tests for YouTube video collection."""

from datetime import UTC, datetime

from app.youtube import YouTubeService, YouTubeVideo, YouTubeVideoMetadata


class StubVideoFeed:
    def __init__(self, videos_by_channel: dict[str, list[YouTubeVideoMetadata]]) -> None:
        self._videos_by_channel = videos_by_channel

    def fetch_recent_videos(self, channel_id: str) -> list[YouTubeVideoMetadata]:
        return self._videos_by_channel[channel_id]


class StubTranscriptProvider:
    def __init__(self, transcripts_by_video: dict[str, str | None]) -> None:
        self._transcripts_by_video = transcripts_by_video

    def fetch_transcript(self, video_id: str) -> str | None:
        return self._transcripts_by_video[video_id]


def test_collect_recent_videos_enriches_feed_entries_with_transcripts() -> None:
    published_at = datetime(2026, 9, 4, 12, 30, tzinfo=UTC)
    metadata = YouTubeVideoMetadata(
        video_id="video-123",
        title="A practical AI update",
        url="https://www.youtube.com/watch?v=video-123",
        channel_name="AI Channel",
        published_at=published_at,
    )
    video_feed = StubVideoFeed({"channel-123": [metadata]})
    transcript_provider = StubTranscriptProvider(
        {"video-123": "A concise transcript."}
    )
    service = YouTubeService(video_feed, transcript_provider)

    videos = service.collect_recent_videos(["channel-123"])

    assert videos == [
        YouTubeVideo(
            video_id="video-123",
            title="A practical AI update",
            url="https://www.youtube.com/watch?v=video-123",
            channel_name="AI Channel",
            published_at=published_at,
            transcript="A concise transcript.",
        )
    ]
