"""Public interface for article aggregation."""

from app.aggregator.models import UserProfile
from app.aggregator.service import ArticleAggregator

__all__ = ["ArticleAggregator", "UserProfile"]
