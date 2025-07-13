from group_sms_chat.domain.exceptions import GroupNotFoundError, UserNotInGroupError
from group_sms_chat.domain.group import GroupName
from group_sms_chat.domain.group_repository import GroupRepository
from group_sms_chat.domain.sms_service import SMSService
from group_sms_chat.domain.user import User


class LeaveGroupHandler:
    def __init__(self, group_repository: GroupRepository, sms_service: SMSService) -> None:
        """
        Initialize the LeaveGroupHandler.

        :param group_repository: An instance of GroupRepository to manage group data.
        :param sms_service: An instance of SMSService to handle SMS operations.
        """
        self.group_service = group_repository
        self.sms_service = sms_service

    async def handle(self, group_name: GroupName, user: User) -> None:
        """
        Handle the leaving of a user from a group.

        :param group_name: The name of the group to leave.
        :param user: The user who wants to leave the group.
        :return: None
        :raises GroupNotFoundError: If the group does not exist.
        :raises UserNotInGroupError: If the user is not a member of the group.
        """
        group = await self.group_service.get_group(group_name)
        if group is None:
            raise GroupNotFoundError(group_name=group_name)

        group_phone_number = group.get_user_phone_number(user.username)
        if group_phone_number is None:
            raise UserNotInGroupError(username=user.username, group_name=group_name)

        group.remove_user(user.username)
        await self.group_service.create_or_update_group(group)

        await self.sms_service.send_sms(
            from_phone_number=group_phone_number,
            to_phone_number=user.phone_number,
            message=f"You have left the group '{group_name}'."
        )
