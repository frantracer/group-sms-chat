import logging

from group_sms_chat.domain.sms_service import SMSService
from group_sms_chat.domain.user import PhoneNumber


class TwilioSMSService(SMSService):
    async def available_phone_numbers(self) -> list[PhoneNumber]:
        return [PhoneNumber("+12345678290"), PhoneNumber("+19187654321")]

    async def send_sms(self, from_phone_number: PhoneNumber, to_phone_number: PhoneNumber, message: str) -> None:
        logging.info(f"Sending SMS from {from_phone_number} to {to_phone_number}: {message}")
