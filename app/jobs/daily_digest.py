"""Composition root and executable command for the daily digest job."""

import logging

from app.aggregator import ArticleAggregator, UserProfile
from app.anthropic_news import AnthropicNewsScraper
from app.article_persistence import ArticlePersistenceService
from app.daily_digest_job import DailyDigestJob
from app.database import (
    SqlAlchemyArticleRepository,
    SqlAlchemyDigestDeliveryHistory,
    create_article_table,
    create_database_engine,
    create_digest_delivery_tables,
)
from app.digest import DigestService
from app.email import DigestEmailComposer, EmailAgent, SmtpEmailSender, SmtpSettings
from app.openai_news import OpenAINewsScraper
from app.personalized_digest import PersonalizedDailyDigestService
from app.personalized_digest_delivery import PersonalizedDigestEmailDeliveryService
from app.pipeline import CollectionPipeline
from app.youtube import YouTubeAtomFeed, YouTubeService, YouTubeTranscriptProvider
from config import Settings

__all__ = ["create_daily_digest_job", "main"]

_LOGGER = logging.getLogger(__name__)


def create_daily_digest_job(settings: Settings) -> DailyDigestJob:
    """Assemble the scheduled job from runtime settings and concrete adapters."""
    _validate_job_settings(settings)

    database_engine = create_database_engine(settings.database_url)
    create_article_table(database_engine)
    create_digest_delivery_tables(database_engine)

    collection_pipeline = CollectionPipeline(
        news_sources=(OpenAINewsScraper(), AnthropicNewsScraper()),
        video_source=YouTubeService(
            video_feed=YouTubeAtomFeed(),
            transcript_provider=YouTubeTranscriptProvider(),
        ),
        youtube_channel_ids=settings.youtube_channel_ids,
        article_persister=ArticlePersistenceService(
            SqlAlchemyArticleRepository(database_engine)
        ),
    )
    digest_generator = PersonalizedDailyDigestService(
        collection_pipeline=collection_pipeline,
        article_aggregator=ArticleAggregator(),
        digest_service=DigestService(),
    )
    digest_delivery = PersonalizedDigestEmailDeliveryService(
        digest_generator=digest_generator,
        email_composer=DigestEmailComposer(),
        email_agent=EmailAgent(
            SmtpEmailSender(
                SmtpSettings(
                    host=settings.smtp_host,
                    port=settings.smtp_port,
                    username=settings.smtp_username,
                    password=settings.smtp_password,
                    sender=settings.smtp_sender,
                )
            )
        ),
        delivery_history=SqlAlchemyDigestDeliveryHistory(database_engine),
    )

    return DailyDigestJob(
        digest_delivery=digest_delivery,
        profile=UserProfile(interests=settings.daily_digest_interests),
        recipient=settings.daily_digest_recipient,
    )


def main() -> None:
    """Run the daily digest once and exit with the resulting process status."""
    logging.basicConfig(level=logging.INFO)
    job = create_daily_digest_job(Settings.from_environment())
    job.run()
    _LOGGER.info("Daily digest job completed")


def _validate_job_settings(settings: Settings) -> None:
    if not settings.daily_digest_recipient:
        raise ValueError("DAILY_DIGEST_RECIPIENT must be configured")
    if not settings.daily_digest_interests:
        raise ValueError("DAILY_DIGEST_INTERESTS must contain at least one interest")

    required_values = {
        "DATABASE_URL": settings.database_url,
        "SMTP_HOST": settings.smtp_host,
        "SMTP_USERNAME": settings.smtp_username,
        "SMTP_PASSWORD": settings.smtp_password,
        "SMTP_SENDER": settings.smtp_sender,
    }
    missing_values = [name for name, value in required_values.items() if not value]

    if missing_values:
        raise ValueError(f"Missing required settings: {', '.join(missing_values)}")


if __name__ == "__main__":
    main()
