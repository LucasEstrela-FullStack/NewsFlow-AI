"""Contract tests for the SQLAlchemy digest delivery-history adapter."""

from datetime import date

from sqlalchemy import create_engine

from app.database import (
    SqlAlchemyDigestDeliveryHistory,
    create_article_table,
    create_digest_delivery_tables,
)
from app.personalized_digest import GeneratedDigest


def test_reserve_stores_a_digest_once_for_a_recipient_and_day() -> None:
    engine = create_engine("sqlite://")
    create_article_table(engine)
    create_digest_delivery_tables(engine)
    repository = SqlAlchemyDigestDeliveryHistory(engine)
    digest = GeneratedDigest(
        content="# NewFlow AI Digest",
        article_ids=(),
    )

    reservation = repository.reserve(
        recipient="reader@example.com",
        delivery_date=date(2026, 9, 9),
        digest=digest,
    )
    duplicate_reservation = repository.reserve(
        recipient="reader@example.com",
        delivery_date=date(2026, 9, 9),
        digest=digest,
    )

    assert reservation is not None
    assert duplicate_reservation is None
