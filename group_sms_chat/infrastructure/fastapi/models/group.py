from pydantic import BaseModel

from group_sms_chat.domain.group import GroupName
from group_sms_chat.domain.user import Username


class Group(BaseModel):
    name: GroupName
    users: list[Username]
