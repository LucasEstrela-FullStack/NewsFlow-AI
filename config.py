"""Application configuration loaded at the composition boundary."""

from dataclasses import dataclass
import os

from dotenv import load_dotenv

__all__ = ["Settings"]


@dataclass(frozen=True, slots=True)
class Settings:
    """Runtime settings used to assemble the Flask application."""

    environment: str = "development"
    debug: bool = False
    secret_key: str = "development-only"
    host: str = "127.0.0.1"
    port: int = 5000
    database_url: str = ""
    smtp_host: str = ""
    smtp_port: int = 465
    smtp_username: str = ""
    smtp_password: str = ""
    smtp_sender: str = ""

    @classmethod
    def from_environment(cls) -> "Settings":
        """Build settings from environment variables and a local .env file."""
        load_dotenv()

        return cls(
            environment=os.getenv("NEWFLOW_ENV", "development"),
            debug=_read_boolean("NEWFLOW_DEBUG", default=False),
            secret_key=os.getenv("SECRET_KEY", "development-only"),
            host=os.getenv("HOST", "127.0.0.1"),
            port=_read_port("PORT", default=5000),
            database_url=os.getenv("DATABASE_URL", ""),
            smtp_host=os.getenv("SMTP_HOST", ""),
            smtp_port=_read_port("SMTP_PORT", default=465),
            smtp_username=os.getenv("SMTP_USERNAME", ""),
            smtp_password=os.getenv("SMTP_PASSWORD", ""),
            smtp_sender=os.getenv("SMTP_SENDER", ""),
        )


def _read_boolean(name: str, *, default: bool) -> bool:
    value = os.getenv(name)
    if value is None:
        return default

    return value.strip().lower() in {"1", "true", "yes", "on"}


def _read_port(name: str, *, default: int) -> int:
    value = os.getenv(name, str(default))

    try:
        port = int(value)
    except ValueError as error:
        raise ValueError(f"{name} must be an integer") from error

    if not 1 <= port <= 65_535:
        raise ValueError(f"{name} must be between 1 and 65535")

    return port
