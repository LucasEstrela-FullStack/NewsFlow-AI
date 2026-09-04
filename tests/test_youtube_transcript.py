"""Contract tests for the YouTube transcript adapter."""

from dataclasses import dataclass

import pytest
from youtube_transcript_api import (
    NoTranscriptFound,
    RequestBlocked,
    TranscriptsDisabled,
)

from app.youtube import YouTubeTranscriptProvider


@dataclass(frozen=True)
class StubTranscriptSnippet:
    text: str


class StubTranscriptApi:
    def __init__(self) -> None:
        self.requests: list[tuple[str, list[str]]] = []

    def fetch(
        self,
        video_id: str,
        languages: list[str],
    ) -> list[StubTranscriptSnippet]:
        self.requests.append((video_id, languages))
        return [
            StubTranscriptSnippet("First sentence."),
            StubTranscriptSnippet(" Second sentence. "),
        ]


class UnavailableTranscriptApi:
    def fetch(
        self,
        video_id: str,
        languages: list[str],
    ) -> list[StubTranscriptSnippet]:
        raise TranscriptsDisabled(video_id)


class BlockedTranscriptApi:
    def fetch(
        self,
        video_id: str,
        languages: list[str],
    ) -> list[StubTranscriptSnippet]:
        raise RequestBlocked(video_id)


class StubAvailableTranscript:
    def fetch(self) -> list[StubTranscriptSnippet]:
        return [StubTranscriptSnippet("Transcripción disponible.")]


class FallbackLanguageTranscriptApi:
    def __init__(self) -> None:
        self.listed_video_ids: list[str] = []

    def fetch(
        self,
        video_id: str,
        languages: list[str],
    ) -> list[StubTranscriptSnippet]:
        raise NoTranscriptFound(video_id, languages, None)

    def list(self, video_id: str) -> list[StubAvailableTranscript]:
        self.listed_video_ids.append(video_id)
        return [StubAvailableTranscript()]


def test_fetch_transcript_joins_normalized_snippets() -> None:
    transcript_api = StubTranscriptApi()
    transcript_provider = YouTubeTranscriptProvider(
        transcript_api=transcript_api,
        languages=("en", "pt"),
    )

    transcript = transcript_provider.fetch_transcript("video-123")

    assert transcript_api.requests == [("video-123", ["en", "pt"])]
    assert transcript == "First sentence. Second sentence."


def test_fetch_transcript_returns_none_when_captions_are_unavailable() -> None:
    transcript_provider = YouTubeTranscriptProvider(
        transcript_api=UnavailableTranscriptApi()
    )

    transcript = transcript_provider.fetch_transcript("video-without-captions")

    assert transcript is None


def test_fetch_transcript_falls_back_to_any_available_language() -> None:
    transcript_api = FallbackLanguageTranscriptApi()
    transcript_provider = YouTubeTranscriptProvider(transcript_api=transcript_api)

    transcript = transcript_provider.fetch_transcript("video-in-spanish")

    assert transcript_api.listed_video_ids == ["video-in-spanish"]
    assert transcript == "Transcripción disponible."


def test_fetch_transcript_does_not_hide_operational_failures() -> None:
    transcript_provider = YouTubeTranscriptProvider(
        transcript_api=BlockedTranscriptApi()
    )

    with pytest.raises(RequestBlocked):
        transcript_provider.fetch_transcript("blocked-video")
