from dataclasses import dataclass
from http import HTTPStatus
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException

from group_sms_chat.application.create_new_group_handler import CreateNewGroupHandler
from group_sms_chat.application.find_groups_handler import FindGroupsHandler
from group_sms_chat.application.join_group_handler import JoinGroupHandler
from group_sms_chat.application.leave_group_handler import LeaveGroupHandler
from group_sms_chat.application.register_user_handler import RegisterUserHandler
from group_sms_chat.application.send_group_message_handler import SendGroupMessageHandler
from group_sms_chat.application.validate_user_password import ValidateUserPasswordHandler
from group_sms_chat.domain.exceptions import (
    PhoneNumberAlreadyExistsError,
    UserAlreadyExistsError,
    UserInvalidCredentialsError,
    UserNotInGroupError,
)
from group_sms_chat.domain.group import GroupName
from group_sms_chat.domain.user import HashedPassword, PhoneNumber, User, Username, UserPassword
from group_sms_chat.infrastructure.fastapi.models.group import Group
from group_sms_chat.infrastructure.fastapi.models.twilio import TwilioIncomingSmsRequest
from group_sms_chat.infrastructure.fastapi.models.user import (
    NewUserRequest,
    NewUserResponse,
)
from group_sms_chat.infrastructure.sqlite.group_repository import SQLiteGroupRepository
from group_sms_chat.infrastructure.sqlite.user_repository import SQLiteUserRepository
from group_sms_chat.infrastructure.twilio.sms_service import TwilioSMSService


@dataclass
class APIHandlers:
    """
    List all the API handlers for the FastAPI application.
    """

    validate_user: ValidateUserPasswordHandler
    register_user: RegisterUserHandler
    create_new_group: CreateNewGroupHandler
    find_groups: FindGroupsHandler
    join_group: JoinGroupHandler
    leave_group: LeaveGroupHandler
    send_group_message: SendGroupMessageHandler


def create_app(handlers: APIHandlers) -> FastAPI:
    """
    Create and return a FastAPI application instance.
    """
    app = FastAPI()

    async def get_user(username: Username, password: UserPassword) -> User:
        """
        Dependency to get the current user.
        """
        try:
            return await handlers.validate_user.handle(username, password)
        except UserInvalidCredentialsError:
            raise HTTPException(
                status_code=HTTPStatus.UNAUTHORIZED,
                detail="Invalid username or password."
            ) from None

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
            ) from None
        except PhoneNumberAlreadyExistsError:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail=f"User with phone number {user.phone_number} already exists."
            ) from None

    @app.get("/groups")
    async def find_groups(group_name: str) -> list[Group]:
        """
        Endpoint to find groups.
        """
        groups = await handlers.find_groups.handle(GroupName(root=group_name))
        return [Group(name=group.name, users=[user.username for user in group.users]) for group in groups]

    @app.post("/groups")
    async def create_group(group_name: GroupName, user: Annotated[User, Depends(get_user)]) -> Group:
        """
        Endpoint to create a new group.
        """
        new_group = await handlers.create_new_group.handle(group_name=group_name, user=user)
        return Group(name=new_group.name, users=[user.username for user in new_group.users])

    @app.post("/groups/{group_name}/users/",
              status_code=HTTPStatus.NO_CONTENT)
    async def join_group(group_name: str, user: Annotated[User, Depends(get_user)]) -> None:
        """
        Endpoint for a user to join a group.
        """
        await handlers.join_group.handle(
            group_name=GroupName(root=group_name),
            user=user)

    @app.delete("/groups/{group_name}/users/",
                status_code=HTTPStatus.NO_CONTENT)
    async def leave_group(group_name: str, user: Annotated[User, Depends(get_user)]) -> None:
        """
        Endpoint for a user to leave a group.
        """
        try:
            await handlers.leave_group.handle(GroupName(root=group_name), user=user)
        except UserNotInGroupError:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=f"User {user.username} is not a member of the group {group_name}."
            ) from None

    @app.post("/webhooks/twilio/sms",
                status_code=HTTPStatus.NO_CONTENT)
    async def handle_twilio_incoming_sms(request: TwilioIncomingSmsRequest) -> None:
        """
        Endpoint to handle incoming SMS messages from Twilio.
        """
        await handlers.send_group_message.handle(
            user_number=PhoneNumber(root=request.from_number),
            group_number=PhoneNumber(root=request.to_number),
            message=request.body
        )

    return app


# Initialize the API handlers
DB_FILE_PATH = "./group_sms_chat.db"
user_repo = SQLiteUserRepository(file_path=DB_FILE_PATH)
group_repo = SQLiteGroupRepository(file_path=DB_FILE_PATH)
sms_service = TwilioSMSService()

handlers = APIHandlers(
    validate_user=ValidateUserPasswordHandler(user_repository=user_repo),
    register_user=RegisterUserHandler(user_repository=user_repo),
    create_new_group=CreateNewGroupHandler(group_repository=group_repo, sms_service=sms_service),
    find_groups=FindGroupsHandler(group_repository=group_repo),
    join_group=JoinGroupHandler(group_repository=group_repo, sms_service=sms_service),
    leave_group=LeaveGroupHandler(group_repository=group_repo, sms_service=sms_service),
    send_group_message=SendGroupMessageHandler(group_repository=group_repo, user_repository=user_repo,
                                               sms_service=sms_service),
)

app = create_app(handlers)
