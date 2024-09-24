from typing import List

from tools.base import BaseEntity, RegisterProtocol
from tools.dbs.models import DBEntityStack
from tools.dbs.tiny import TiDBCache


def db_records_to_entity(register: RegisterProtocol, stack: DBEntityStack) -> List[BaseEntity]:
    if stack.data:
        return [register.get_cls(item.setting.type)(**item.model_dump()) for item in stack.data]
    else:
        return []