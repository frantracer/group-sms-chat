import sqlite3

from group_sms_chat.domain.group import Group, GroupName
from group_sms_chat.domain.group_repository import GroupRepository
from group_sms_chat.domain.user import PhoneNumber, Username


class SQLiteGroupRepository(GroupRepository):
    def __init__(self, file_path: str) -> None:
        self.file_path = file_path

        self.connection = sqlite3.connect(file_path)
        self.connection.execute(
            "CREATE TABLE IF NOT EXISTS group_users ("
            "    group_name TEXT NOT NULL,"
            "    username TEXT NOT NULL,"
            "    user_group_phone_number TEXT NOT NULL,"
            "    PRIMARY KEY (group_name, username))"
        )
        self.connection.commit()

    async def create_or_update_group(self, group: Group) -> None:
        # This approach is very inefficient, because it deletes the group and then re-inserts all users
        # However, it is simple and works for small groups.
        cursor = self.connection.cursor()
        cursor.execute("DELETE FROM group_users WHERE group_name = ?", (str(group.name),))
        for user in group.users:
            cursor.execute(
                "INSERT INTO group_users (group_name, username, user_group_phone_number) VALUES (?, ?, ?)",
                (str(group.name), str(user.username), str(user.user_group_phone_number))
            )
        self.connection.commit()

    async def get_group(self, group_name: GroupName) -> Group | None:
        cursor = self.connection.cursor()
        cursor.execute("SELECT group_name, username, user_group_phone_number "
                       "FROM group_users WHERE group_name = ?", (str(group_name),))
        rows = cursor.fetchall()

        if not rows:
            return None

        group = Group(name=group_name)
        for row in rows:
            _, username, user_group_phone_number = row
            group.add_user(
                user=Username(root=username), phone_number=PhoneNumber(root=user_group_phone_number)
            )

        return group

    async def find_groups_by_name(self, name: GroupName) -> list[Group]:
        cursor = self.connection.cursor()
        cursor.execute("SELECT group_name, username, user_group_phone_number "
                       "FROM group_users "
                       "WHERE LOWER(group_name) LIKE ?", (f"%{str(name).lower()}%",))
        rows = cursor.fetchall()

        groups: dict[GroupName, Group] = {}
        for row in rows:
            group_name, username, user_group_phone_number = row
            if group_name not in groups:
                groups[group_name] = Group(name=GroupName(root=group_name))
            groups[group_name].add_user(
                user=Username(root=username), phone_number=PhoneNumber(root=user_group_phone_number)
            )

        return list(groups.values())

    async def find_user_groups(self, username: Username) -> list[Group]:
        cursor = self.connection.cursor()
        cursor.execute("SELECT group_name, username, user_group_phone_number "
                       "FROM group_users WHERE username = ?", (str(username),))
        rows = cursor.fetchall()

        groups = {}
        for row in rows:
            group_name, _, user_group_phone_number = row
            if group_name not in groups:
                groups[group_name] = Group(name=GroupName(root=group_name))
            groups[group_name].add_user(
                user=username, phone_number=PhoneNumber(root=user_group_phone_number)
            )

        return list(groups.values())

    async def delete_group(self, group_name: GroupName) -> None:
        cursor = self.connection.cursor()
        cursor.execute("DELETE FROM group_users WHERE group_name = ?", (str(group_name),))
        self.connection.commit()

    async def get_user_group_by_user_and_phone(
            self, username: Username, phone_number: PhoneNumber
    ) -> Group | None:
        cursor = self.connection.cursor()
        cursor.execute(
            "SELECT group_name FROM group_users "
            "WHERE username = ? AND user_group_phone_number = ?",
            (str(username), str(phone_number))
        )
        row = cursor.fetchone()
        if row:
            return await self.get_group(GroupName(root=row[0]))
        return None
