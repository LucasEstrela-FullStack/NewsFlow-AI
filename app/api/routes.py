"""Operational HTTP endpoints."""

from flask import Blueprint

api_blueprint = Blueprint("api", __name__)


@api_blueprint.get("/health")
def health_check() -> tuple[dict[str, str], int]:
    """Report whether the web process is ready to receive requests."""
    return {"service": "newflow", "status": "ok"}, 200
