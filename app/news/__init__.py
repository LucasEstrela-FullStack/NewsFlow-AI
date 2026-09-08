"""Public interface for shared news concepts."""

from app.news.markdown import ArticleMarkdownProcessor
from app.news.models import NewsArticle

__all__ = ["ArticleMarkdownProcessor", "NewsArticle"]
