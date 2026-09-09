"""Public interface for email composition and delivery."""

from app.email.composer import DigestEmailComposer
from app.email.models import EmailMessage
from app.email.service import EmailAgent

__all__ = ["DigestEmailComposer", "EmailAgent", "EmailMessage"]
