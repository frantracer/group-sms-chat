from pydantic import BaseModel, Field, RootModel

from group_sms_chat.domain.user import PhoneNumber, Username


class GroupName(RootModel[str]):
    root: str = Field(min_length=3, max_length=20, pattern=r"^[a-z0-9._-]+$")

    def __str__(self) -> str:
        return str(self.root)


class GroupUser(BaseModel):
    username: Username
    user_group_phone_number: PhoneNumber

    def __hash__(self) -> int:
        return hash(str(self.username) + str(self.user_group_phone_number))


class Group(BaseModel):
    name: GroupName
    users: set[GroupUser] = Field(default_factory=set)

    def get_user_phone_number(self, username: Username) -> PhoneNumber | None:
        """
        Get the phone number of a user in the group by their UUID.

        :param username: The UUID of the user.
        :return: The phone number of the user or None if the user is not in the group.
        """
        for user in self.users:
            if user.username == username:
                return user.user_group_phone_number
        return None

    def add_user(self, user: Username, phone_number: PhoneNumber) -> None:
        """
        Add a user to the group.

        :param user: The username of the user to add to the group.
        :param phone_number: The phone number of the user to add to the group.
        """
        self.users.add(GroupUser(
            username=user,
            user_group_phone_number=phone_number
        ))

    def remove_user(self, username: Username) -> None:
        """
        Remove a user from the group.

        :param username: The username of the user to remove from the group.
        """
        self.users = {user for user in self.users if user.username != username}
