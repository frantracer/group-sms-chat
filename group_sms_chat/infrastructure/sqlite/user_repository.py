import sqlite3

from group_sms_chat.domain.exceptions import (
    PhoneNumberAlreadyExistsError,
    UnhandledError,
    UserAlreadyExistsError,
)
from group_sms_chat.domain.user import User, Username
from group_sms_chat.domain.user_repository import UserRepository


class SQLiteUserRepository(UserRepository):
    def __init__(self, file_path: str) -> None:
        self.connection = sqlite3.connect(file_path)
        self.connection.execute(
            "CREATE TABLE IF NOT EXISTS users "
            "(username TEXT PRIMARY KEY, phone_number TEXT NOT NULL UNIQUE, hashed_password TEXT)"
        )
        self.connection.commit()

    async def add_user(self, user: User) -> None:
        try:
            cursor = self.connection.cursor()
            cursor.execute(
                "INSERT INTO users (username, phone_number, hashed_password) VALUES (?, ?, ?)",
                (str(user.username), str(user.phone_number), str(user.hashed_password))
            )
            self.connection.commit()
        except sqlite3.IntegrityError as e:
            if "UNIQUE constraint failed" in str(e):
                if "username" in str(e):
                    raise UserAlreadyExistsError(username=user.username) from e
                if "phone_number" in str(e):
                    raise PhoneNumberAlreadyExistsError(phone_number=user.phone_number) from e
            raise UnhandledError(message=str(e)) from e

    async def get_user(self, username: Username) -> User | None:
        cursor = self.connection.cursor()
        cursor.execute("SELECT username, phone_number, hashed_password FROM users WHERE username = ?", (str(username),))
        row = cursor.fetchone()
        if row:
            return User(username=Username(root=row[0]), phone_number=row[1], hashed_password=row[2])
        return None

    async def delete_user(self, username: Username) -> None:
        cursor = self.connection.cursor()
        cursor.execute("DELETE FROM users WHERE username = ?", (str(username),))
        self.connection.commit()
