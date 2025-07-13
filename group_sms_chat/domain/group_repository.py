from abc import ABC, abstractmethod

from group_sms_chat.domain.group import Group, GroupName
from group_sms_chat.domain.user import Username


class GroupRepository(ABC):

    @abstractmethod
    async def create_or_update_group(self, group: Group) -> None:
        """
        Create a new group.
        :param group: The group to create.
        """
        ...

    @abstractmethod
    async def find_groups_by_name(self, name: GroupName) -> list[Group]:
        """
        Find groups by their name. The search is case-insensitive and matches any part of the name.
        :param name: The name of the group to search for.
        :return: A list of groups that match the name.
        """
        ...

    @abstractmethod
    async def find_user_groups(self, username: Username) -> list[Group]:
        """
        Find all groups that a user belongs to.

        :param user_uuid: The UUID of the user.
        :return: A list of groups that the user belongs to.
        """
        ...
