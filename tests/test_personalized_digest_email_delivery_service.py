"""Behavior tests for personalized digest email delivery."""

from collections.abc import Sequence
from datetime import UTC, datetime

from app.aggregator import ArticleAggregator, UserProfile
from app.digest import DigestService
from app.email import DigestEmailComposer, EmailAgent, EmailMessage
from app.news import NewsArticle
from app.personalized_digest import PersonalizedDailyDigestService
from app.personalized_digest_delivery import PersonalizedDigestEmailDeliveryService
from app.pipeline import CollectionPipeline
from app.youtube.models import YouTubeVideo


class StaticNewsSource:
    """Deterministic source with general and profile-relevant articles."""

    def fetch_recent_articles(self) -> list[NewsArticle]:
        return [
            NewsArticle(
                article_id="company-update",
                title="Company update",
                url="https://example.com/company-update",
                description="General company information.",
                category="Company",
                published_at=datetime(2026, 9, 9, tzinfo=UTC),
                source="OpenAI",
            ),
            NewsArticle(
                article_id="agent-research",
                title="Reliable agents research",
                url="https://example.com/agent-research",
                description="A research update about AI agents.",
                category="Research",
                published_at=datetime(2026, 9, 9, tzinfo=UTC),
                source="Anthropic",
            ),
        ]


class EmptyVideoSource:
    """Video source that keeps the collection pipeline deterministic."""

    def collect_recent_videos(self, channel_ids: Sequence[str]) -> list[YouTubeVideo]:
        return []


class InMemoryEmailSender:
    """External email boundary fake that records delivered messages."""

    def __init__(self) -> None:
        self.delivered_messages: list[EmailMessage] = []

    def send(self, message: EmailMessage) -> None:
        self.delivered_messages.append(message)


def test_send_delivers_a_digest_personalized_for_the_recipient(
    article_persister,
) -> None:
    collection_pipeline = CollectionPipeline(
        news_sources=[StaticNewsSource()],
        video_source=EmptyVideoSource(),
        youtube_channel_ids=[],
        article_persister=article_persister,
    )
    digest_generator = PersonalizedDailyDigestService(
        collection_pipeline=collection_pipeline,
        article_aggregator=ArticleAggregator(),
        digest_service=DigestService(),
    )
    sender = InMemoryEmailSender()
    service = PersonalizedDigestEmailDeliveryService(
        digest_generator=digest_generator,
        email_composer=DigestEmailComposer(),
        email_agent=EmailAgent(sender=sender),
    )

    service.send(
        profile=UserProfile(interests=("agents",)),
        recipient="reader@example.com",
    )

    assert sender.delivered_messages == [
        EmailMessage(
            recipient="reader@example.com",
            subject="Your NewFlow AI Daily Digest",
            body=(
                "# NewFlow AI Digest\n\n"
                "# Reliable agents research\n\n"
                "- Source: Anthropic\n"
                "- Category: Research\n"
                "- Published at: 2026-09-09T00:00:00+00:00\n"
                "- Original URL: https://example.com/agent-research\n\n"
                "## Description\n\n"
                "A research update about AI agents.\n\n"
                "---\n\n"
                "# Company update\n\n"
                "- Source: OpenAI\n"
                "- Category: Company\n"
                "- Published at: 2026-09-09T00:00:00+00:00\n"
                "- Original URL: https://example.com/company-update\n\n"
                "## Description\n\n"
                "General company information."
            ),
        )
    ]
