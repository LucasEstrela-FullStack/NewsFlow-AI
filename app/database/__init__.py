"""Database infrastructure adapters."""

from app.database.connection import create_database_engine
from app.database.articles import SqlAlchemyArticleRepository, create_article_table
from app.database.digest_deliveries import (
    SqlAlchemyDigestDeliveryHistory,
    create_digest_delivery_tables,
)

__all__ = [
    "SqlAlchemyArticleRepository",
    "SqlAlchemyDigestDeliveryHistory",
    "create_article_table",
    "create_database_engine",
    "create_digest_delivery_tables",
]
