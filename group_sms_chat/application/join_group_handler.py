from group_sms_chat.domain.exceptions import GroupNotFoundError, MaximumNumberOfGroupsReachedError
from group_sms_chat.domain.group import GroupName
from group_sms_chat.domain.group_repository import GroupRepository
from group_sms_chat.domain.sms_service import SMSService
from group_sms_chat.domain.user import PhoneNumber, User


class JoinGroupHandler:
    def __init__(self, group_repository: GroupRepository, sms_service: SMSService) -> None:
        """
        Initialize the JoinGroupHandler.

        :param group_repository: An instance of GroupRepository to manage group data.
        :param sms_service: An instance of SMSService to send SMS notifications.
        """
        self.group_repository = group_repository
        self.sms_service = sms_service

    async def handle(self, group_name: GroupName, user: User) -> None:
        """
        Handle the joining of a user to a group.
        :param group_name: The name of the group to join.
        :param user: The user who wants to join the group.
        :return: None
        :raises GroupNotFoundError: If the group does not exist.
        :raises MaximumNumberOfGroupsReachedError: If the user has reached the maximum number of groups they can join.
        """
        group = await self.group_repository.get_group(group_name)
        if group is None:
            raise GroupNotFoundError(group_name=group_name)

        current_groups = await self.group_repository.find_user_groups(user.username)
        available_phone_numbers = await self.sms_service.available_phone_numbers()

        if len(current_groups) >= len(available_phone_numbers):
            raise MaximumNumberOfGroupsReachedError(username=user.username, max_number=len(available_phone_numbers))

        used_phone_numbers = [group.get_user_phone_number(user.username) for group in current_groups]

        phone_number = find_available_phone_number(
            used_numbers=[phone_number for phone_number in used_phone_numbers if phone_number is not None],
            available_numbers=available_phone_numbers
        )
        if phone_number is None:
            raise MaximumNumberOfGroupsReachedError(username=user.username, max_number=len(available_phone_numbers))

        group.add_user(user.username, phone_number)
        await self.group_repository.create_or_update_group(group)

        await self.sms_service.send_sms(
            from_phone_number=phone_number,
            to_phone_number=user.phone_number,
            message=f"You have joined the group '{group_name}'. "
                    f"Reply to this message to send text messages to the members of the group."
        )


def find_available_phone_number(
        used_numbers: list[PhoneNumber],
        available_numbers: list[PhoneNumber]
) -> PhoneNumber | None:
    """
    Find an available phone number from the list of available phone numbers.
    :param used_numbers: A list of phone numbers that are already in use.
    :param available_numbers: A list of available phone numbers.
    :return: An available phone number or None if no available number is found.
    """
    for number in available_numbers:
        if number not in used_numbers:
            return number
    return None
