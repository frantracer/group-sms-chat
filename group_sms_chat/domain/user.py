import hashlib

from pydantic import BaseModel, Field, RootModel


class Username(RootModel[str]):
    root: str = Field(min_length=3, max_length=20, pattern=r"^[a-z0-9._-]+$")

    def __str__(self) -> str:
        return str(self.root)


class PhoneNumber(RootModel[str]):
    root: str = Field(min_length=10, max_length=15, pattern=r"^\+?[0-9]\d{1,14}$")

    def __str__(self) -> str:
        return str(self.root)


class HashedPassword(RootModel[str]):
    root: str = Field(min_length=128, max_length=128, pattern=r"^[a-zA-Z0-9./]+$")

    def __str__(self) -> str:
        return str(self.root)

    @classmethod
    def from_string(cls, password: str) -> "HashedPassword":
        """
        Create a HashedPassword instance from a string.
        This is useful for converting raw password strings into hashed passwords.
        """
        return cls(root=hashlib.sha512(password.encode("utf-8")).hexdigest())


class User(BaseModel):
    """
    Represents a user in the system.
    """

    username: Username
    phone_number: PhoneNumber
    hashed_password: HashedPassword
