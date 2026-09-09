"""Tests for application configuration."""

from config import Settings


def test_settings_reads_database_url_from_environment(monkeypatch) -> None:
    monkeypatch.setenv(
        "DATABASE_URL",
        "postgresql://newflow:secret@localhost:5432/newflow",
    )

    settings = Settings.from_environment()

    assert settings.database_url == "postgresql://newflow:secret@localhost:5432/newflow"


def test_settings_reads_smtp_connection_details_from_environment(monkeypatch) -> None:
    monkeypatch.setenv("SMTP_HOST", "smtp.example.test")
    monkeypatch.setenv("SMTP_PORT", "465")
    monkeypatch.setenv("SMTP_USERNAME", "newsflow")
    monkeypatch.setenv("SMTP_SENDER", "newsflow@example.com")

    settings = Settings.from_environment()

    assert settings.smtp_host == "smtp.example.test"
    assert settings.smtp_port == 465
    assert settings.smtp_username == "newsflow"
    assert settings.smtp_sender == "newsflow@example.com"
