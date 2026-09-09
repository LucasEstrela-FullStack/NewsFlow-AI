"""Personalized digest email delivery use case."""

from app.aggregator import UserProfile
from app.personalized_digest_delivery.ports import (
    EmailComposer,
    EmailDeliveryAgent,
    PersonalizedDigestGenerator,
)

__all__ = ["PersonalizedDigestEmailDeliveryService"]


class PersonalizedDigestEmailDeliveryService:
    """Generate and deliver a personalized daily digest by email."""

    def __init__(
        self,
        digest_generator: PersonalizedDigestGenerator,
        email_composer: EmailComposer,
        email_agent: EmailDeliveryAgent,
    ) -> None:
        self._digest_generator = digest_generator
        self._email_composer = email_composer
        self._email_agent = email_agent

    def send(self, profile: UserProfile, recipient: str) -> None:
        """Generate a digest for the profile and deliver it to the recipient."""
        digest = self._digest_generator.generate(profile)
        email_message = self._email_composer.compose(recipient, digest)

        self._email_agent.send(email_message)
