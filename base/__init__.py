from typing import List

from pydantic import BaseModel
from abc import ABC

class BaseEntity(BaseModel, ABC):
    _entity_type: str
    _entity_attr: str
    _entity_match_type: str

    @property
    def additional_fields(self) -> List[str]:
        """
        Return list of attributes that will be map on the entity properties
        """
        return [attr for attr in self.__dict__.keys() if attr != self._entity_attr]