"""Behavior tests for digest delivery history."""

from datetime import date

import pytest

from app.aggregator import UserProfile
from app.digest_delivery_history import DigestDeliveryReservation
from app.email import DigestEmailComposer, EmailAgent, EmailMessage
from app.personalized_digest import GeneratedDigest
from app.personalized_digest_delivery import PersonalizedDigestEmailDeliveryService


class StaticDigestGenerator:
    """Deterministic digest boundary for delivery-history tests."""

    def generate(self, _: UserProfile) -> GeneratedDigest:
        return GeneratedDigest(
            content="# NewFlow AI Digest\n\n# Agents update",
            article_ids=("agents-1",),
        )


class InMemoryEmailSender:
    """External email boundary substitute."""

    def __init__(self) -> None:
        self.delivered_messages: list[EmailMessage] = []

    def send(self, message: EmailMessage) -> None:
        self.delivered_messages.append(message)


class UnavailableEmailSender:
    """External email boundary substitute that fails deterministically."""

    def send(self, _: EmailMessage) -> None:
        raise ConnectionError("SMTP is unavailable")


class InMemoryDigestDeliveryHistory:
    """Delivery-history boundary substitute with daily deduplication."""

    def __init__(self) -> None:
        self._reserved_keys: set[tuple[str, date]] = set()
        self.statuses: list[str] = []

    def reserve(
        self,
        recipient: str,
        delivery_date: date,
        _: GeneratedDigest,
    ) -> DigestDeliveryReservation | None:
        key = (recipient, delivery_date)
        if key in self._reserved_keys:
            return None

        self._reserved_keys.add(key)
        return DigestDeliveryReservation(identifier=len(self._reserved_keys))

    def mark_sent(self, _: DigestDeliveryReservation) -> None:
        self.statuses.append("sent")

    def mark_failed(self, _: DigestDeliveryReservation) -> None:
        self.statuses.append("failed")


def test_send_records_a_delivery_once_for_the_same_recipient_and_day() -> None:
    sender = InMemoryEmailSender()
    history = InMemoryDigestDeliveryHistory()
    service = PersonalizedDigestEmailDeliveryService(
        digest_generator=StaticDigestGenerator(),
        email_composer=DigestEmailComposer(),
        email_agent=EmailAgent(sender=sender),
        delivery_history=history,
        current_date=lambda: date(2026, 9, 9),
    )

    profile = UserProfile(interests=("agents",))
    service.send(profile=profile, recipient="reader@example.com")
    service.send(profile=profile, recipient="reader@example.com")

    assert sender.delivered_messages == [
        EmailMessage(
            recipient="reader@example.com",
            subject="Your NewFlow AI Daily Digest",
            body="# NewFlow AI Digest\n\n# Agents update",
        )
    ]
    assert history.statuses == ["sent"]


def test_send_marks_a_reserved_delivery_as_failed_when_email_delivery_fails() -> None:
    history = InMemoryDigestDeliveryHistory()
    service = PersonalizedDigestEmailDeliveryService(
        digest_generator=StaticDigestGenerator(),
        email_composer=DigestEmailComposer(),
        email_agent=EmailAgent(sender=UnavailableEmailSender()),
        delivery_history=history,
        current_date=lambda: date(2026, 9, 9),
    )

    with pytest.raises(ConnectionError, match="SMTP is unavailable"):
        service.send(
            profile=UserProfile(interests=("agents",)),
            recipient="reader@example.com",
        )

    assert history.statuses == ["failed"]
