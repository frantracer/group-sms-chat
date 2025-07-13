from group_sms_chat.domain.exceptions import UserInvalidCredentialsError
from group_sms_chat.domain.user import User, Username, UserPassword
from group_sms_chat.domain.user_repository import UserRepository


class ValidateUserPasswordHandler:
    """
    Handler for validating user credentials.
    """

    def __init__(self, user_repository: UserRepository) -> None:
        """
        Initialize the handler with a user repository.
        :param user_repository: An instance of UserRepository to interact with user data.
        """
        self.user_repository = user_repository

    async def handle(self, username: Username, password: UserPassword) -> User:
        """
        Validate the user's password against the stored credentials.
        :param username: Username of the user to validate.
        :param password: Password of the user to validate.
        :return: User object if credentials are valid.
        :raises UserInvalidCredentialsError: If the username does not exist or the password is incorrect.
        """
        user = await self.user_repository.get_user(username)
        if not user:
            raise UserInvalidCredentialsError(username)

        if user.check_password(password):
            return user
        raise UserInvalidCredentialsError(username)
