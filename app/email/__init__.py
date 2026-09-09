"""Public interface for email composition and delivery."""

from app.email.composer import DigestEmailComposer
from app.email.models import EmailMessage

__all__ = ["DigestEmailComposer", "EmailMessage"]
