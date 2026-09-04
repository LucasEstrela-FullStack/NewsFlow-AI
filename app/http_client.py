"""Shared HTTP transport for text-based external sources."""

from urllib.request import Request, urlopen

__all__ = ["download_text"]


def download_text(url: str) -> str:
    """Download UTF-8 text using the application's transport defaults."""
    request = Request(url, headers={"User-Agent": "NewFlow/1.0"})
    with urlopen(request, timeout=15) as response:
        return response.read().decode("utf-8")
