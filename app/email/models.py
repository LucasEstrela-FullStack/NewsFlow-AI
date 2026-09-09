"""Domain models for email delivery."""

from dataclasses import dataclass

__all__ = ["EmailMessage"]


@dataclass(frozen=True, slots=True)
class EmailMessage:
    """A fully composed email ready for delivery."""

    recipient: str
    subject: str
    body: str
