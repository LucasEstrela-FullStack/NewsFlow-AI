"""Behavior tests for the scheduled daily digest job."""

from app.aggregator import UserProfile
from app.daily_digest_job import DailyDigestJob


class RecordingDigestDelivery:
    """Delivery boundary substitute for scheduled-job tests."""

    def __init__(self) -> None:
        self.deliveries: list[tuple[UserProfile, str]] = []

    def send(self, profile: UserProfile, recipient: str) -> None:
        self.deliveries.append((profile, recipient))


def test_run_delivers_the_digest_for_the_configured_recipient() -> None:
    profile = UserProfile(interests=("agents", "research"))
    delivery = RecordingDigestDelivery()
    job = DailyDigestJob(
        digest_delivery=delivery,
        profile=profile,
        recipient="reader@example.com",
    )

    job.run()

    assert delivery.deliveries == [(profile, "reader@example.com")]
