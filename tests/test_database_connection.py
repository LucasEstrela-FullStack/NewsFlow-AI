"""Tests for the PostgreSQL infrastructure adapter."""

import pytest

from app.database.connection import create_database_engine


def test_create_database_engine_configures_the_given_postgresql_url() -> None:
    engine = create_database_engine(
        "postgresql://newflow:secret@localhost:5432/newflow"
    )

    assert engine.url.render_as_string(hide_password=False) == (
        "postgresql://newflow:secret@localhost:5432/newflow"
    )


@pytest.mark.parametrize("database_url", ["", "   "])
def test_create_database_engine_rejects_an_empty_database_url(database_url: str) -> None:
    with pytest.raises(ValueError, match="DATABASE_URL must not be empty"):
        create_database_engine(database_url)
