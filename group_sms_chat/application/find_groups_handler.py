from group_sms_chat.domain.group import Group, GroupName
from group_sms_chat.domain.group_repository import GroupRepository


class FindGroupsHandler:
    def __init__(self, group_repository: GroupRepository) -> None:
        """
        Initialize the FindGroupsHandler.

        :param group_repository: An instance of GroupRepository to manage group data.
        """
        self.group_repository = group_repository

    async def handle(self, group_name: GroupName) -> list[Group]:
        """
        Handle the search for groups by name.

        :param group_name: The name of the group to search for.
        :return: A list of groups that match the given name.
        """
        return await self.group_repository.find_groups_by_name(group_name)
