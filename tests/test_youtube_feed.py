"""Contract tests for the YouTube Atom feed adapter."""

from datetime import UTC, datetime

from app.youtube import YouTubeAtomFeed, YouTubeVideoMetadata


ATOM_FEED = """\
<?xml version="1.0" encoding="UTF-8"?>
<feed xmlns="http://www.w3.org/2005/Atom"
      xmlns:yt="http://www.youtube.com/xml/schemas/2015">
  <entry>
    <yt:videoId>video-123</yt:videoId>
    <title>A practical AI update</title>
    <link rel="alternate" href="https://www.youtube.com/watch?v=video-123" />
    <author><name>AI Channel</name></author>
    <published>2026-09-04T12:30:00+00:00</published>
  </entry>
</feed>
"""


def test_fetch_recent_videos_maps_atom_entries_to_metadata() -> None:
    requested_urls: list[str] = []

    def download_feed(url: str) -> str:
        requested_urls.append(url)
        return ATOM_FEED

    video_feed = YouTubeAtomFeed(download_feed=download_feed)

    videos = video_feed.fetch_recent_videos(" channel-123 ")

    assert requested_urls == [
        "https://www.youtube.com/feeds/videos.xml?channel_id=channel-123"
    ]
    assert videos == [
        YouTubeVideoMetadata(
            video_id="video-123",
            title="A practical AI update",
            url="https://www.youtube.com/watch?v=video-123",
            channel_name="AI Channel",
            published_at=datetime(2026, 9, 4, 12, 30, tzinfo=UTC),
        )
    ]
