"""Domain models for digest delivery history."""

from dataclasses import dataclass

__all__ = ["DigestDeliveryReservation"]


@dataclass(frozen=True, slots=True)
class DigestDeliveryReservation:
    """Identifies a delivery reserved for a recipient on a given day."""

    identifier: int
