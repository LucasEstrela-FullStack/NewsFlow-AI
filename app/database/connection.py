"""PostgreSQL connection factory."""

from sqlalchemy import Engine, create_engine

__all__ = ["create_database_engine"]


def create_database_engine(database_url: str) -> Engine:
    """Create the database engine configured for NewFlow."""
    if not database_url.strip():
        raise ValueError("DATABASE_URL must not be empty")

    return create_engine(database_url, pool_pre_ping=True)
