"""Domain models produced by personalized digest generation."""

from dataclasses import dataclass

__all__ = ["GeneratedDigest"]


@dataclass(frozen=True, slots=True)
class GeneratedDigest:
    """Rendered digest content and the articles represented in it."""

    content: str
    article_ids: tuple[str, ...]
