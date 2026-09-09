"""Personalized digest email delivery use case."""

from collections.abc import Callable
from datetime import UTC, date, datetime

from app.aggregator import UserProfile
from app.digest_delivery_history import DigestDeliveryHistory
from app.personalized_digest_delivery.ports import (
    EmailComposer,
    EmailDeliveryAgent,
    PersonalizedDigestGenerator,
)

__all__ = ["PersonalizedDigestEmailDeliveryService"]


class PersonalizedDigestEmailDeliveryService:
    """Generate and deliver a personalized daily digest by email."""

    def __init__(
        self,
        digest_generator: PersonalizedDigestGenerator,
        email_composer: EmailComposer,
        email_agent: EmailDeliveryAgent,
        delivery_history: DigestDeliveryHistory,
        current_date: Callable[[], date] | None = None,
    ) -> None:
        self._digest_generator = digest_generator
        self._email_composer = email_composer
        self._email_agent = email_agent
        self._delivery_history = delivery_history
        self._current_date = current_date or _utc_today

    def send(self, profile: UserProfile, recipient: str) -> None:
        """Generate a digest for the profile and deliver it to the recipient."""
        digest = self._digest_generator.generate(profile)
        reservation = self._delivery_history.reserve(
            recipient,
            self._current_date(),
            digest,
        )
        if reservation is None:
            return

        email_message = self._email_composer.compose(recipient, digest.content)
        try:
            self._email_agent.send(email_message)
        except Exception:
            self._delivery_history.mark_failed(reservation)
            raise

        self._delivery_history.mark_sent(reservation)


def _utc_today() -> date:
    return datetime.now(UTC).date()
