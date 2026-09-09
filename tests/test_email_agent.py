"""Behavior tests for email delivery."""

from app.email import EmailAgent, EmailMessage


class InMemoryEmailSender:
    """Email boundary fake that records delivered messages."""

    def __init__(self) -> None:
        self.delivered_messages: list[EmailMessage] = []

    def send(self, message: EmailMessage) -> None:
        self.delivered_messages.append(message)


def test_send_delivers_the_composed_email_message() -> None:
    sender = InMemoryEmailSender()
    agent = EmailAgent(sender=sender)
    message = EmailMessage(
        recipient="reader@example.com",
        subject="Your NewFlow AI Daily Digest",
        body="# NewFlow AI Digest",
    )

    agent.send(message)

    assert sender.delivered_messages == [message]
