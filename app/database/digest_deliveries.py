"""SQLAlchemy adapter for digest delivery history."""

from datetime import UTC, date, datetime

from sqlalchemy import (
    BigInteger,
    CheckConstraint,
    Column,
    Date,
    DateTime,
    Engine,
    ForeignKey,
    Identity,
    Integer,
    String,
    Table,
    Text,
    UniqueConstraint,
    insert,
    update,
)
from sqlalchemy.engine import Connection
from sqlalchemy.exc import IntegrityError

from app.database.articles import _metadata
from app.digest_delivery_history import DigestDeliveryReservation
from app.personalized_digest import GeneratedDigest

__all__ = ["SqlAlchemyDigestDeliveryHistory", "create_digest_delivery_tables"]

_delivery_identifier = BigInteger().with_variant(Integer, "sqlite")
_digest_deliveries = Table(
    "digest_deliveries",
    _metadata,
    Column("id", _delivery_identifier, Identity(always=True), primary_key=True),
    Column("recipient", Text, nullable=False),
    Column("delivery_date", Date, nullable=False),
    Column("content", Text, nullable=False),
    Column("status", String(20), nullable=False, default="pending"),
    Column("created_at", DateTime(timezone=True), nullable=False),
    UniqueConstraint("recipient", "delivery_date", name="uq_digest_delivery_recipient_day"),
    CheckConstraint(
        "status IN ('pending', 'sent', 'failed')",
        name="ck_digest_delivery_status",
    ),
)
_digest_delivery_articles = Table(
    "digest_delivery_articles",
    _metadata,
    Column(
        "delivery_id",
        ForeignKey("digest_deliveries.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "article_id",
        ForeignKey("articles.article_id", ondelete="RESTRICT"),
        primary_key=True,
    ),
)


def create_digest_delivery_tables(engine: Engine) -> None:
    """Create digest delivery-history tables when they do not exist yet."""
    _metadata.create_all(
        engine,
        tables=[_digest_deliveries, _digest_delivery_articles],
    )


class SqlAlchemyDigestDeliveryHistory:
    """Persist digest delivery reservations using SQLAlchemy Core."""

    def __init__(self, engine: Engine) -> None:
        self._engine = engine

    def reserve(
        self,
        recipient: str,
        delivery_date: date,
        digest: GeneratedDigest,
    ) -> DigestDeliveryReservation | None:
        """Reserve one recipient-day delivery or report that it already exists."""
        with self._engine.begin() as connection:
            try:
                with connection.begin_nested():
                    result = connection.execute(
                        insert(_digest_deliveries).values(
                            recipient=recipient,
                            delivery_date=delivery_date,
                            content=digest.content,
                            status="pending",
                            created_at=datetime.now(UTC),
                        )
                    )
                    identifier = int(result.inserted_primary_key[0])
                    self._store_article_links(connection, identifier, digest.article_ids)
            except IntegrityError:
                return None

        return DigestDeliveryReservation(identifier=identifier)

    def mark_sent(self, reservation: DigestDeliveryReservation) -> None:
        """Mark a reserved delivery as successfully sent."""
        self._set_status(reservation, "sent")

    def mark_failed(self, reservation: DigestDeliveryReservation) -> None:
        """Mark a reserved delivery as failed."""
        self._set_status(reservation, "failed")

    def _store_article_links(
        self,
        connection: Connection,
        delivery_identifier: int,
        article_ids: tuple[str, ...],
    ) -> None:
        if article_ids:
            connection.execute(
                insert(_digest_delivery_articles),
                [
                    {"delivery_id": delivery_identifier, "article_id": article_id}
                    for article_id in article_ids
                ],
            )

    def _set_status(self, reservation: DigestDeliveryReservation, status: str) -> None:
        with self._engine.begin() as connection:
            connection.execute(
                update(_digest_deliveries)
                .where(_digest_deliveries.c.id == reservation.identifier)
                .values(status=status)
            )
