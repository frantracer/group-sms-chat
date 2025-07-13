from http import HTTPStatus

from fastapi.testclient import TestClient

from group_sms_chat.app import create_app


def test_api_health_check() -> None:
    client = TestClient(create_app())
    response = client.get("/health")
    assert response.status_code == HTTPStatus.OK
