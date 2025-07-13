from pydantic import BaseModel


class TwilioIncomingSmsRequest(BaseModel):
    from_number: str
    to_number: str
    body: str
