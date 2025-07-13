from group_sms_chat.domain.user import User
from group_sms_chat.domain.user_repository import UserRepository


class RegisterUserHandler:
    def __init__(self, user_repository: UserRepository) -> None:
        self.user_repository = user_repository

    async def handle(self, new_user: User) -> None:
        """
        Handle the registration of a new user.
        :param new_user: The user to be registered.
        :return: None
        :raises UserAlreadyExistsError: If a user with the same username already exists.
        :raises PhoneNumberAlreadyExistsError: If a user with the same phone number already exists.
        """
        await self.user_repository.add_user(new_user)
