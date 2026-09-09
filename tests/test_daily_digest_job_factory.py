"""Tests for scheduled daily digest job configuration."""

import pytest

from app.jobs.daily_digest import create_daily_digest_job
from config import Settings


def test_create_daily_digest_job_requires_a_recipient() -> None:
    with pytest.raises(ValueError, match="DAILY_DIGEST_RECIPIENT"):
        create_daily_digest_job(Settings())


def test_create_daily_digest_job_requires_profile_interests() -> None:
    settings = Settings(daily_digest_recipient="reader@example.com")

    with pytest.raises(ValueError, match="DAILY_DIGEST_INTERESTS"):
        create_daily_digest_job(settings)
