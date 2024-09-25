from typing import List

from pydantic import Field

from tools.base import BaseEntity, BaseEntityStack


class DBEntity(BaseEntity, extra='allow'):
    pass


class DBEntityStack(BaseEntityStack):
    data: List[DBEntity] = Field(default_factory=list)