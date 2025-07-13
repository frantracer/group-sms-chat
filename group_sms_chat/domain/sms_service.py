from abc import ABC, abstractmethod

from group_sms_chat.domain.user import PhoneNumber


class SMSService(ABC):

    @abstractmethod
    async def available_phone_numbers(self) -> list[PhoneNumber]:
        """
        Retrieve a list of available phone numbers that can be used to send SMS messages.

        :return: A list of available phone numbers.
        """
        ...

    @abstractmethod
    async def send_sms(
            self,
            from_phone_number: PhoneNumber,
            to_phone_number: PhoneNumber,
            message: str
    ) -> None:
        """
        Send an SMS message to a given phone number.

        :param from_phone_number: The phone number from which the SMS is sent.
        :param to_phone_number: The phone number to which the SMS is sent.
        :param message: The content of the SMS message.
        """
        ...
