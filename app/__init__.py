"""NewFlow application factory."""

from flask import Flask

from app.api import api_blueprint
from config import Settings

__all__ = ["create_app"]


def create_app(settings: Settings | None = None) -> Flask:
    """Create and configure a NewFlow application instance."""
    current_settings = settings or Settings.from_environment()

    application = Flask(__name__)
    application.config.from_mapping(
        ENVIRONMENT=current_settings.environment,
        DEBUG=current_settings.debug,
        SECRET_KEY=current_settings.secret_key,
        HOST=current_settings.host,
        PORT=current_settings.port,
    )
    application.register_blueprint(api_blueprint)

    return application
