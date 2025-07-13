from pydantic import BaseModel


class NewUserRequest(BaseModel):
    password: str
    username: str
    phone_number: str


class LoginRequest(BaseModel):
    password: str
    username: str
