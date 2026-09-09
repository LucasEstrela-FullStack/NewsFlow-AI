"""Domain models for article aggregation."""

from dataclasses import dataclass

__all__ = ["UserProfile"]


@dataclass(frozen=True, slots=True)
class UserProfile:
    """Topics that determine an article's relevance for a user."""

    interests: tuple[str, ...]
