from group_sms_chat.domain.exceptions import PhoneNotFoundError
from group_sms_chat.domain.group_repository import GroupRepository
from group_sms_chat.domain.sms_service import SMSService
from group_sms_chat.domain.user import PhoneNumber
from group_sms_chat.domain.user_repository import UserRepository


class SendGroupMessageHandler:
    def __init__(self, user_repository: UserRepository,
                 group_repository: GroupRepository,
                 sms_service: SMSService) -> None:
        self.user_repository = user_repository
        self.group_repository = group_repository
        self.sms_service = sms_service

    async def handle(self, user_number: PhoneNumber, group_number: PhoneNumber, message: str) -> None:
        """
        Handle sending a group message.
        :param user_number: The phone number of the sender.
        :param group_number: The phone number of the group.
        :param message: The message to be sent.
        :return: None

        """
        user = await self.user_repository.get_user_by_phone_number(user_number)
        if user is None:
            raise PhoneNotFoundError(user_number)

        group = await self.group_repository.get_user_group_by_user_and_phone(user.username, group_number)
        if group is None:
            raise PhoneNotFoundError(group_number)

        new_message = f"{user.username}: {message}"
        for group_user in group.users:
            if group_user.username == user.username:
                continue

            sending_user = await self.user_repository.get_user(group_user.username)
            if sending_user is None:
                continue

            await self.sms_service.send_sms(from_phone_number=group_user.user_group_phone_number,
                                            to_phone_number=sending_user.phone_number,
                                            message=new_message)
