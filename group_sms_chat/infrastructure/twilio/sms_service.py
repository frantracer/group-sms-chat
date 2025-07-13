import logging

from twilio.rest import Client  # type: ignore[import-untyped]

from group_sms_chat.domain.sms_service import SMSService
from group_sms_chat.domain.user import PhoneNumber


class TwilioSMSService(SMSService):
    def __init__(self, account_sid: str, auth_token: str, phone_numbers: list[str]) -> None:
        self.account_sid = account_sid
        self.auth_token = auth_token
        self.client = Client(account_sid, auth_token)
        self._phone_numbers = [PhoneNumber(root=num) for num in phone_numbers]

    async def available_phone_numbers(self) -> list[PhoneNumber]:
        return list(self._phone_numbers)

    async def send_sms(self, from_phone_number: PhoneNumber, to_phone_number: PhoneNumber, message: str) -> None:
        logging.info(f"Sending SMS from {from_phone_number} to {to_phone_number}: {message}")
        self.client.messages.create(
            body=message,
            from_=str(from_phone_number),
            to=str(to_phone_number)
        )
