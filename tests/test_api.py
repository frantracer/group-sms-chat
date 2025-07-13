from http import HTTPStatus
from unittest.mock import AsyncMock

import pytest
from fastapi.testclient import TestClient

from group_sms_chat.app import APIHandlers, create_app
from group_sms_chat.application.create_new_group_handler import CreateNewGroupHandler
from group_sms_chat.application.find_groups_handler import FindGroupsHandler
from group_sms_chat.application.join_group_handler import JoinGroupHandler
from group_sms_chat.application.leave_group_handler import LeaveGroupHandler
from group_sms_chat.application.register_user_handler import RegisterUserHandler
from group_sms_chat.application.validate_user_password import ValidateUserPasswordHandler


@pytest.fixture
def handlers() -> APIHandlers:
    return APIHandlers(
        validate_user=AsyncMock(spec=ValidateUserPasswordHandler),
        register_user=AsyncMock(spec=RegisterUserHandler),
        create_new_group=AsyncMock(spec=CreateNewGroupHandler),
        find_groups=AsyncMock(spec=FindGroupsHandler),
        join_group=AsyncMock(spec=JoinGroupHandler),
        leave_group=AsyncMock(spec=LeaveGroupHandler),
    )


def test_api_health_check(handlers: APIHandlers) -> None:
    client = TestClient(create_app(handlers))
    response = client.get("/health")
    assert response.status_code == HTTPStatus.OK
