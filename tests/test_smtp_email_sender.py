"""Behavior tests for SMTP email delivery."""

from email.message import EmailMessage as MimeEmailMessage

from app.email import EmailMessage, SmtpEmailSender, SmtpSettings


class InMemorySmtpClient:
    """SMTP boundary fake that records sent MIME messages."""

    def __init__(self) -> None:
        self.credentials: tuple[str, str] | None = None
        self.sent_messages: list[MimeEmailMessage] = []

    def __enter__(self) -> "InMemorySmtpClient":
        return self

    def __exit__(self, *_: object) -> None:
        return None

    def login(self, username: str, password: str) -> None:
        self.credentials = (username, password)

    def send_message(self, message: MimeEmailMessage) -> None:
        self.sent_messages.append(message)


def test_send_delivers_a_composed_message_through_smtp() -> None:
    smtp_client = InMemorySmtpClient()
    sender = SmtpEmailSender(
        settings=SmtpSettings(
            host="smtp.example.com",
            port=465,
            username="mailer@example.com",
            password="smtp-password",
            sender="mailer@example.com",
        ),
        client_factory=lambda _host, _port: smtp_client,
    )

    sender.send(
        EmailMessage(
            recipient="reader@example.com",
            subject="Your NewFlow AI Daily Digest",
            body="# NewFlow AI Digest",
        )
    )

    sent_message = smtp_client.sent_messages[0]
    assert smtp_client.credentials == ("mailer@example.com", "smtp-password")
    assert sent_message["From"] == "mailer@example.com"
    assert sent_message["To"] == "reader@example.com"
    assert sent_message["Subject"] == "Your NewFlow AI Daily Digest"
    assert sent_message.get_content().strip() == "# NewFlow AI Digest"
