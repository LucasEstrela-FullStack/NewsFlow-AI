"""Digest creation use case."""

from app.news import ArticleMarkdownProcessor, NewsArticle

__all__ = ["DigestService"]


class DigestService:
    """Combine normalized articles into a single Markdown digest."""

    def create(self, articles: list[NewsArticle]) -> str:
        """Return a Markdown digest containing the supplied articles."""
        article_markdown = ArticleMarkdownProcessor()
        rendered_articles = [
            article_markdown.to_markdown(article) for article in articles
        ]

        return "# NewFlow AI Digest\n\n" + "\n\n---\n\n".join(rendered_articles)
