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


def test_settings_reads_daily_digest_profile_from_environment(monkeypatch) -> None:
    monkeypatch.setenv("DAILY_DIGEST_RECIPIENT", "reader@example.com")
    monkeypatch.setenv("DAILY_DIGEST_INTERESTS", "agents, research, agents")
    monkeypatch.setenv("YOUTUBE_CHANNEL_IDS", "channel-one, channel-two")

    settings = Settings.from_environment()

    assert settings.daily_digest_recipient == "reader@example.com"
    assert settings.daily_digest_interests == ("agents", "research")
    assert settings.youtube_channel_ids == ("channel-one", "channel-two")
