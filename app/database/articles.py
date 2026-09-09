"""SQLAlchemy adapter for article persistence."""

from sqlalchemy import Column, DateTime, Engine, MetaData, String, Table, Text, select

from app.news import NewsArticle

__all__ = ["SqlAlchemyArticleRepository", "create_article_table"]

_metadata = MetaData()
_articles = Table(
    "articles",
    _metadata,
    Column("article_id", String(255), primary_key=True),
    Column("title", String(500), nullable=False),
    Column("url", Text, nullable=False),
    Column("description", Text, nullable=True),
    Column("category", String(255), nullable=True),
    Column("published_at", DateTime(timezone=True), nullable=False),
    Column("source", String(255), nullable=False),
)


def create_article_table(engine: Engine) -> None:
    """Create the article table when it does not exist yet."""
    _metadata.create_all(engine, tables=[_articles])


class SqlAlchemyArticleRepository:
    """Stores articles using SQLAlchemy Core without leaking ORM records inward."""

    def __init__(self, engine: Engine) -> None:
        self._engine = engine

    def save(self, articles: list[NewsArticle]) -> int:
        """Insert only articles whose identifiers are not stored yet."""
        unique_articles = {article.article_id: article for article in articles}
        if not unique_articles:
            return 0

        with self._engine.begin() as connection:
            existing_article_ids = set(
                connection.scalars(
                    select(_articles.c.article_id).where(
                        _articles.c.article_id.in_(unique_articles)
                    )
                )
            )
            new_articles = [
                article
                for article_id, article in unique_articles.items()
                if article_id not in existing_article_ids
            ]
            if new_articles:
                connection.execute(_articles.insert(), [_to_record(article) for article in new_articles])

        return len(new_articles)


def _to_record(article: NewsArticle) -> dict[str, object]:
    return {
        "article_id": article.article_id,
        "title": article.title,
        "url": article.url,
        "description": article.description,
        "category": article.category,
        "published_at": article.published_at,
        "source": article.source,
    }
