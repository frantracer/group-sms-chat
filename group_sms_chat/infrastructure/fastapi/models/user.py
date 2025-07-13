from pydantic import BaseModel

from group_sms_chat.domain.user import PhoneNumber, Username


class NewUserRequest(BaseModel):
    password: str
    username: Username
    phone_number: PhoneNumber


class NewUserResponse(BaseModel):
    username: Username
    phone_number: PhoneNumber

class LoginRequest(BaseModel):
    password: str
    username: str
