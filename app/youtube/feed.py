"""YouTube Atom feed adapter."""

from collections.abc import Callable
from datetime import datetime
from urllib.parse import urlencode
from xml.etree import ElementTree

from app.http_client import download_text
from app.youtube.models import YouTubeVideoMetadata

__all__ = ["YouTubeAtomFeed", "YouTubeFeedError"]

_ATOM_NAMESPACE = "http://www.w3.org/2005/Atom"
_YOUTUBE_NAMESPACE = "http://www.youtube.com/xml/schemas/2015"
_FEED_ENDPOINT = "https://www.youtube.com/feeds/videos.xml"


class YouTubeFeedError(RuntimeError):
    """Raised when a YouTube channel feed cannot be interpreted."""


class YouTubeAtomFeed:
    """Read recent video metadata from YouTube's public Atom feed."""

    def __init__(
        self,
        download_feed: Callable[[str], str] | None = None,
    ) -> None:
        self._download_feed = download_feed or download_text

    def fetch_recent_videos(self, channel_id: str) -> list[YouTubeVideoMetadata]:
        normalized_channel_id = channel_id.strip()
        if not normalized_channel_id:
            raise ValueError("channel_id cannot be empty")

        query = urlencode({"channel_id": normalized_channel_id})
        feed_content = self._download_feed(f"{_FEED_ENDPOINT}?{query}")

        try:
            root = ElementTree.fromstring(feed_content)
            return [self._map_entry(entry) for entry in root.findall(_atom("entry"))]
        except (ElementTree.ParseError, ValueError) as error:
            raise YouTubeFeedError(
                f"Invalid YouTube feed for channel {normalized_channel_id!r}"
            ) from error

    @staticmethod
    def _map_entry(entry: ElementTree.Element) -> YouTubeVideoMetadata:
        return YouTubeVideoMetadata(
            video_id=_required_text(entry, _youtube("videoId")),
            title=_required_text(entry, _atom("title")),
            url=_alternate_link(entry),
            channel_name=_required_text(entry, f"{_atom('author')}/{_atom('name')}"),
            published_at=_published_at(entry),
        )


def _required_text(entry: ElementTree.Element, path: str) -> str:
    element = entry.find(path)
    if element is None or not element.text or not element.text.strip():
        raise ValueError(f"Missing required feed field: {path}")

    return element.text.strip()


def _alternate_link(entry: ElementTree.Element) -> str:
    for link in entry.findall(_atom("link")):
        if link.get("rel") == "alternate" and link.get("href"):
            return str(link.get("href"))

    raise ValueError("Missing alternate video link")


def _published_at(entry: ElementTree.Element) -> datetime:
    value = _required_text(entry, _atom("published"))
    published_at = datetime.fromisoformat(value.replace("Z", "+00:00"))

    if published_at.tzinfo is None:
        raise ValueError("Published timestamp must include a timezone")

    return published_at


def _atom(tag: str) -> str:
    return f"{{{_ATOM_NAMESPACE}}}{tag}"


def _youtube(tag: str) -> str:
    return f"{{{_YOUTUBE_NAMESPACE}}}{tag}"
