from uuid import UUID

from pydantic import BaseModel


class Group(BaseModel):
    uuid: UUID
    name: str
