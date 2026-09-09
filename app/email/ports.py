"""Dependencies required to deliver email messages."""

from typing import Protocol

from app.email.models import EmailMessage

__all__ = ["EmailSender"]


class EmailSender(Protocol):
    """Deliver a composed email message through an external provider."""

    def send(self, message: EmailMessage) -> None: ...
