from group_sms_chat.domain.user import PhoneNumber, Username


class UnhandledError(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)


class UserAlreadyExistsError(Exception):
    def __init__(self, username: Username) -> None:
        super().__init__(f"User with username '{username}' already exists.")


class PhoneNumberAlreadyExistsError(Exception):
    def __init__(self, phone_number: PhoneNumber) -> None:
        super().__init__(f"User with phone number '{phone_number}' already exists.")


class MaximumNumberOfGroupsReachedError(Exception):
    def __init__(self, username: Username, max_number: int) -> None:
        super().__init__(f"User '{username}' has reached the maximum number {max_number} of groups they can join.")


class UserInvalidCredentialsError(Exception):
    def __init__(self, username: Username) -> None:
        super().__init__(f"Invalid credentials for user '{username}'. Please check your username and password.")
