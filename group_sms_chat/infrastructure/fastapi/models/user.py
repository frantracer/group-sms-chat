from pydantic import BaseModel

from group_sms_chat.domain.user import PhoneNumber, Username, UserPassword


class NewUserRequest(BaseModel):
    password: UserPassword
    username: Username
    phone_number: PhoneNumber


class NewUserResponse(BaseModel):
    username: Username
    phone_number: PhoneNumber
