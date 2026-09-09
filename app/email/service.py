"""Email delivery use case."""

from app.email.models import EmailMessage
from app.email.ports import EmailSender

__all__ = ["EmailAgent"]


class EmailAgent:
    """Deliver composed email messages through a configured sender."""

    def __init__(self, sender: EmailSender) -> None:
        self._sender = sender

    def send(self, message: EmailMessage) -> None:
        """Deliver an email message through the configured sender."""
        self._sender.send(message)
