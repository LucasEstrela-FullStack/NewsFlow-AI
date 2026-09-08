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

    @classmethod
    def from_environment(cls) -> "Settings":
        """Build settings from environment variables and a local .env file."""
        load_dotenv()

        return cls(
            environment=os.getenv("NEWFLOW_ENV", "development"),
            debug=_read_boolean("NEWFLOW_DEBUG", default=False),
            secret_key=os.getenv("SECRET_KEY", "development-only"),
            host=os.getenv("HOST", "127.0.0.1"),
            port=_read_port(),
            database_url=os.getenv("DATABASE_URL", ""),
        )


def _read_boolean(name: str, *, default: bool) -> bool:
    value = os.getenv(name)
    if value is None:
        return default

    return value.strip().lower() in {"1", "true", "yes", "on"}


def _read_port() -> int:
    value = os.getenv("PORT", "5000")

    try:
        port = int(value)
    except ValueError as error:
        raise ValueError("PORT must be an integer") from error

    if not 1 <= port <= 65_535:
        raise ValueError("PORT must be between 1 and 65535")

    return port
