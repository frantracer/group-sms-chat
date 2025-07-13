from typing import Any

from fastapi.applications import FastAPI

from group_sms_chat.infrastructure.fastapi.models.group import Group
from group_sms_chat.infrastructure.fastapi.models.user import (
    LoginRequest,
    NewUserRequest,
)


def create_app() -> FastAPI:
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

    @app.post("/register")
    async def register_user(user: NewUserRequest) -> Any:
        """
        Endpoint to register a new user.
        """
        return {"message": "User registered successfully", "user": user}

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


app = create_app()
