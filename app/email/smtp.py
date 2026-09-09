"""SMTP adapter for email delivery."""

from collections.abc import Callable
from dataclasses import dataclass
from email.message import EmailMessage as MimeEmailMessage
from smtplib import SMTP_SSL
from typing import Protocol

from app.email.models import EmailMessage

__all__ = ["SmtpEmailSender", "SmtpSettings"]


@dataclass(frozen=True, slots=True)
class SmtpSettings:
    """Connection details for an SMTP email provider."""

    host: str
    port: int
    username: str
    password: str
    sender: str


class SmtpClient(Protocol):
    """Minimal SMTP client behavior required by this adapter."""

    def __enter__(self) -> "SmtpClient": ...

    def __exit__(self, *_: object) -> None: ...

    def login(self, username: str, password: str) -> None: ...

    def send_message(self, message: MimeEmailMessage) -> None: ...


class SmtpEmailSender:
    """Deliver email messages through an SMTP-over-SSL provider."""

    def __init__(
        self,
        settings: SmtpSettings,
        client_factory: Callable[[str, int], SmtpClient] = SMTP_SSL,
    ) -> None:
        self._settings = settings
        self._client_factory = client_factory

    def send(self, message: EmailMessage) -> None:
        """Authenticate and deliver a composed email through SMTP."""
        with self._client_factory(self._settings.host, self._settings.port) as client:
            client.login(self._settings.username, self._settings.password)
            client.send_message(self._to_mime_message(message))

    def _to_mime_message(self, message: EmailMessage) -> MimeEmailMessage:
        mime_message = MimeEmailMessage()
        mime_message["From"] = self._settings.sender
        mime_message["To"] = message.recipient
        mime_message["Subject"] = message.subject
        mime_message.set_content(message.body)

        return mime_message
