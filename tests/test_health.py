"""Tests for operational HTTP endpoints."""

from flask.testing import FlaskClient


def test_health_check_reports_service_as_available(client: FlaskClient) -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.get_json() == {
        "service": "newflow",
        "status": "ok",
    }
