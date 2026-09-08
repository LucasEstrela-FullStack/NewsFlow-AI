"""Tests for application configuration."""

from config import Settings


def test_settings_reads_database_url_from_environment(monkeypatch) -> None:
    monkeypatch.setenv(
        "DATABASE_URL",
        "postgresql://newflow:secret@localhost:5432/newflow",
    )

    settings = Settings.from_environment()

    assert settings.database_url == "postgresql://newflow:secret@localhost:5432/newflow"
