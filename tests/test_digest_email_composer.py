"""Behavior tests for digest email composition."""

from app.email import DigestEmailComposer, EmailMessage


def test_compose_creates_an_email_message_for_a_daily_digest() -> None:
    digest = "# NewFlow AI Digest\n\n# Agent research"

    message = DigestEmailComposer().compose(
        recipient="reader@example.com",
        digest=digest,
    )

    assert message == EmailMessage(
        recipient="reader@example.com",
        subject="Your NewFlow AI Daily Digest",
        body="# NewFlow AI Digest\n\n# Agent research",
    )
