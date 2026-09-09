"""Dependencies required to deliver a personalized digest by email."""

from typing import Protocol

from app.aggregator import UserProfile
from app.email.models import EmailMessage
from app.personalized_digest.models import GeneratedDigest

__all__ = ["EmailComposer", "EmailDeliveryAgent", "PersonalizedDigestGenerator"]


class PersonalizedDigestGenerator(Protocol):
    """Generate a Markdown digest for a user profile."""

    def generate(self, profile: UserProfile) -> GeneratedDigest: ...


class EmailComposer(Protocol):
    """Compose a delivery-ready email containing a digest."""

    def compose(self, recipient: str, digest: str) -> EmailMessage: ...


class EmailDeliveryAgent(Protocol):
    """Deliver a composed email message."""

    def send(self, message: EmailMessage) -> None: ...
