from abc import ABC, abstractmethod

from group_sms_chat.domain.user import User, Username


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
    async def delete_user(self, username: Username) -> None:
        """
        Delete a user by their username.
        """
        ...
