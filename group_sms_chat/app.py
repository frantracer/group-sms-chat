from dataclasses import dataclass
from http import HTTPStatus
from typing import Any

from fastapi.applications import FastAPI, HTTPException

from group_sms_chat.application.register_user_handler import RegisterUserHandler
from group_sms_chat.domain.exceptions import UserAlreadyExistsError, PhoneNumberAlreadyExistsError
from group_sms_chat.domain.user import HashedPassword, User
from group_sms_chat.infrastructure.fastapi.models.group import Group
from group_sms_chat.infrastructure.fastapi.models.user import (
    LoginRequest,
    NewUserRequest, NewUserResponse,
)
from group_sms_chat.infrastructure.sqlite.user_repository import SQLiteUserRepository


@dataclass
class APIHandlers:
    """
    List all the API handlers for the FastAPI application.
    """

    register_user: RegisterUserHandler


def create_app(handlers: APIHandlers) -> FastAPI:
    """
    Create and return a FastAPI application instance.
    """
    app = FastAPI()

    @app.get("/health")
    async def health_check() -> dict[str, str]:
        """
        Health check endpoint to verify if the service is running.
        """
        return {"status": "ok"}

    @app.post("/register",
              status_code=HTTPStatus.CREATED
              )
    async def register_user(user: NewUserRequest) -> NewUserResponse:
        """
        Endpoint to register a new user.
        """
        try:
            await handlers.register_user.handle(User(
                username=user.username,
                phone_number=user.phone_number,
                hashed_password=HashedPassword.from_string(user.password)
            ))
            return NewUserResponse(username=user.username, phone_number=user.phone_number)
        except UserAlreadyExistsError:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail=f"User with username {user.username} already exists."
            )
        except PhoneNumberAlreadyExistsError:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail=f"User with phone number {user.phone_number} already exists."
            )

    @app.post("/login")
    async def login_user(user: LoginRequest) -> Any:
        """
        Endpoint to log in a user.
        """
        return {"message": "User logged in successfully", "user": user}

    @app.get("/groups")
    async def find_groups() -> list[Group]:
        """
        Endpoint to find groups.
        """
        return []

    @app.post("/groups")
    async def create_group(group: Group) -> Group:
        """
        Endpoint to create a new group.
        """
        return Group(uuid=group.uuid, name=group.name)

    @app.post("/groups/{group_uuid}/users/{username}")
    async def join_group(group_uuid: str, username: str) -> Any:
        """
        Endpoint for a user to join a group.
        """
        return {"message": f"User {username} joined group {group_uuid}"}

    @app.delete("/groups/{group_uuid}/users/{username}")
    async def leave_group(group_uuid: str, username: str) -> Any:
        """
        Endpoint for a user to leave a group.
        """
        return {"message": f"User {username} left group {group_uuid}"}

    return app


# Initialize the API handlers
user_repo = SQLiteUserRepository(file_path="./group_sms_chat.db")

handlers = APIHandlers(
    register_user=RegisterUserHandler(user_repository=user_repo)
)

app = create_app(handlers)
