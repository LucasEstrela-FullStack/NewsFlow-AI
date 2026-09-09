"""Use case for running one scheduled daily digest delivery."""

from app.aggregator import UserProfile
from app.daily_digest_job.ports import DigestDelivery

__all__ = ["DailyDigestJob"]


class DailyDigestJob:
    """Deliver a daily digest using a configured profile and recipient."""

    def __init__(
        self,
        digest_delivery: DigestDelivery,
        profile: UserProfile,
        recipient: str,
    ) -> None:
        self._digest_delivery = digest_delivery
        self._profile = profile
        self._recipient = recipient

    def run(self) -> None:
        """Execute one digest delivery."""
        self._digest_delivery.send(self._profile, self._recipient)
