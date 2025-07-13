from abc import ABC, abstractmethod

from group_sms_chat.domain.user import PhoneNumber, User, Username


class UserRepository(ABC):
    @abstractmethod
    async def add_user(self, user: User) -> None:
        """
        Add a new user to the repository.
        """
        ...

    @abstractmethod
    async def get_user(self, username: Username) -> User | None:
        """
        Retrieve a user by their username.
        """
        ...

    @abstractmethod
    async def get_user_by_phone_number(self, phone_number: PhoneNumber) -> User | None:
        """
        Retrieve a user by their phone number.
        """
        ...

    @abstractmethod
    async def delete_user(self, username: Username) -> None:
        """
        Delete a user by their username.
        """
        ...
