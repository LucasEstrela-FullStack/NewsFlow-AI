"""Daily digest email composition."""

from app.email.models import EmailMessage

__all__ = ["DigestEmailComposer"]


class DigestEmailComposer:
    """Compose an email message containing a daily digest."""

    def compose(self, recipient: str, digest: str) -> EmailMessage:
        """Return the daily digest as a ready-to-deliver email message."""
        return EmailMessage(
            recipient=recipient,
            subject="Your NewFlow AI Daily Digest",
            body=digest,
        )
