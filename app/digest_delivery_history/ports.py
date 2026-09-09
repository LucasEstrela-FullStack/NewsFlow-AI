"""Application-owned boundary for recording digest deliveries."""

from datetime import date
from typing import Protocol

from app.digest_delivery_history.models import DigestDeliveryReservation
from app.personalized_digest.models import GeneratedDigest

__all__ = ["DigestDeliveryHistory"]


class DigestDeliveryHistory(Protocol):
    """Reserves and records the outcome of daily digest deliveries."""

    def reserve(
        self,
        recipient: str,
        delivery_date: date,
        digest: GeneratedDigest,
    ) -> DigestDeliveryReservation | None: ...

    def mark_sent(self, reservation: DigestDeliveryReservation) -> None: ...

    def mark_failed(self, reservation: DigestDeliveryReservation) -> None: ...
