"""YouTube transcript adapter."""

from collections.abc import Iterable, Sequence
from typing import Protocol

from youtube_transcript_api import (
    NoTranscriptFound,
    TranscriptsDisabled,
    YouTubeTranscriptApi,
)

__all__ = ["YouTubeTranscriptProvider"]


class TranscriptSnippet(Protocol):
    """Minimum transcript snippet shape required by this adapter."""

    @property
    def text(self) -> str: ...


class AvailableTranscript(Protocol):
    """A transcript advertised as available by YouTube."""

    def fetch(self) -> Iterable[TranscriptSnippet]: ...


class TranscriptApi(Protocol):
    """Minimum API surface required from the transcript library."""

    def fetch(
        self,
        video_id: str,
        languages: list[str],
    ) -> Iterable[TranscriptSnippet]: ...

    def list(self, video_id: str) -> Iterable[AvailableTranscript]: ...


class YouTubeTranscriptProvider:
    """Retrieve and normalize transcripts using youtube-transcript-api."""

    def __init__(
        self,
        transcript_api: TranscriptApi | None = None,
        languages: Sequence[str] = ("en", "pt"),
    ) -> None:
        self._transcript_api = transcript_api or YouTubeTranscriptApi()
        self._languages = list(languages)

    def fetch_transcript(self, video_id: str) -> str | None:
        try:
            snippets = self._fetch_preferred_or_any_language(video_id)
            transcript = " ".join(
                snippet.text.strip() for snippet in snippets if snippet.text.strip()
            )
            return transcript or None
        except TranscriptsDisabled:
            return None

    def _fetch_preferred_or_any_language(
        self,
        video_id: str,
    ) -> Iterable[TranscriptSnippet]:
        try:
            return self._transcript_api.fetch(
                video_id,
                languages=self._languages,
            )
        except NoTranscriptFound:
            available_transcripts = iter(self._transcript_api.list(video_id))
            fallback = next(available_transcripts, None)
            return fallback.fetch() if fallback else ()
