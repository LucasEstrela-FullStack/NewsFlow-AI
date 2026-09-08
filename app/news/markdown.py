"""Markdown representation for collected news articles."""

from app.news.models import NewsArticle

__all__ = ["ArticleMarkdownProcessor"]


class ArticleMarkdownProcessor:
    """Convert normalized article metadata into a digest-ready Markdown document."""

    def to_markdown(self, article: NewsArticle) -> str:
        """Return a deterministic Markdown representation of an article."""
        metadata = [
            f"- Source: {article.source}",
            f"- Published at: {article.published_at.isoformat()}",
            f"- Original URL: {article.url}",
        ]
        if article.category:
            metadata.insert(1, f"- Category: {article.category}")

        sections = [f"# {article.title}", "\n".join(metadata)]
        if article.description:
            sections.append(f"## Description\n\n{article.description}")

        return "\n\n".join(sections)
