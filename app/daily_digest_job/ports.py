"""Application-owned boundaries for the scheduled digest job."""

from typing import Protocol

from app.aggregator import UserProfile

__all__ = ["DigestDelivery"]


class DigestDelivery(Protocol):
    """Delivers a generated digest for a recipient profile."""

    def send(self, profile: UserProfile, recipient: str) -> None: ...
