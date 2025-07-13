from http import HTTPStatus
from unittest.mock import AsyncMock

import pytest
from fastapi.testclient import TestClient

from group_sms_chat.app import APIHandlers, create_app
from group_sms_chat.application.register_user_handler import RegisterUserHandler


@pytest.fixture
def handlers() -> APIHandlers:
    return APIHandlers(
        register_user=AsyncMock(spec=RegisterUserHandler)
    )


def test_api_health_check(handlers: APIHandlers) -> None:
    client = TestClient(create_app(handlers))
    response = client.get("/health")
    assert response.status_code == HTTPStatus.OK
