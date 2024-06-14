from abc import ABC
from typing import Callable, Union, Dict, List, Type, Literal
from uuid import uuid4
from pydantic import BaseModel, Field

from tools.utils import hash_fn


class EntitySetting(BaseModel):
    type: str
    main_attribute: str
    match: Literal['strict', 'loose']


class BaseEntity(BaseModel, ABC):
    """
    Base entity / inheritance and template type

    """
    _internal_fields: List[str] = ['setting', 'icon', 'display_info', 'note']
    setting: EntitySetting
    uuid: str = Field(default_factory=lambda: str(uuid4()))
    icon: str = Field(default='')
    display_info: str = Field(default='')
    note: str = Field(default='')

    @property
    def property_fields(self) -> List[str]:
        """
        Return list
         of attributes that will be map on the entity properties
        """
        return [attr for attr in self.__dict__.keys() if attr not in self._internal_fields]

    def __hash__(self):
        data_to_hash = {name: self.__getattribute__(name) for name in self.property_fields}
        return hash_fn(data_to_hash)


class BaseEntityStack(BaseModel, ABC):
    results: int
    data: List[BaseEntity]

    def filter_by_types(self, types: List[Type[BaseEntity]], inplace: bool = False):
        filtered = [instance for instance in self.data if type(instance) in types]

        if inplace:
            self.data = filtered
        else:
            return filtered


class BaseRegisterFactory(BaseModel):
    items: Dict[str, Union[BaseModel, Callable, str]] = Field(default_factory=dict)

    def register(self, name: str, item: Union[BaseModel, Callable, str]) -> None:
        self.items[name.lower()] = item

    def get_item(self, name: str) -> Union[BaseModel, Callable]:
        return self.items.get(name.lower())

    def get_list_of_names(self):
        return [name.upper() for name in self.items.keys()]

    def __getattr__(self, name: str) -> Union[BaseModel, Callable]:
        item = self.get_item(name)
        if item is not None:
            return item


class EntityRegister(BaseRegisterFactory):
    pass


global entity_register
entity_register = EntityRegister()


class EntitiesTypeNames(BaseRegisterFactory):
    """
    name: name of the class property
    item: maltego type name like "cnd.Entity"
    """
    items: Dict[str, str] = Field(default_factory=dict)


global ENTITIES_TYPE_NAMES
ENTITIES_TYPE_NAMES = EntitiesTypeNames()