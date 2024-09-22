from abc import ABC
from typing import Callable, Union, Dict, List, Type, Literal,Protocol
from uuid import uuid4
from pydantic import BaseModel, Field, field_validator, model_validator
from tools.utils import hash_fn
from enum import Enum


class EntityStackProtocol(Protocol):
    results: int
    data: list[BaseModel]


class RegisterProtocol(Protocol):

    def register(self, name: str, item: Union[BaseModel, Callable, str]) -> None:
        ...

    def get_item(self, name: str) -> Union[BaseModel, Callable]:
        ...

    def get_list_of_names(self) -> List[str]:
        ...


class MaltegoSettingAttributes(BaseModel):
    """
    Base type to set dynamically distinguish trough type check which fields will be set as entity properties and which
    are entity settings
    """
    pass

class EntitySetting(MaltegoSettingAttributes):
    """
    Setting to generate mltego entity
    type: maltego type name e.g. "cnd.Entity"
    main_attribute: main attribute that will be displayed in the maltego entity as primary field
    match: strict or loose
    """
    type: str
    main_attribute: str
    match: Literal['strict', 'loose']


class EntityDisplay(MaltegoSettingAttributes):
    value: str
    position: Enum
    overlay_type: Enum

class EntityIcon(MaltegoSettingAttributes):
    url: str


class EntityNote(MaltegoSettingAttributes):
    note: str


class EntityDisplayInfo(MaltegoSettingAttributes):
    content: str
    title: str


class BaseEntity(BaseModel):
    """
    Base entity / inheritance and template type

    """
    _internal_fields: List[str] = ['setting', 'icon', 'display_info', 'note']
    setting: EntitySetting = Field(..., exclude=True)
    uuid: str = Field(default_factory=lambda: str(uuid4()))
    icon: str | EntityIcon = Field(default='', exclude=True)
    display_info: str | EntityDisplayInfo = Field(default='', exclude=True)
    note: str | EntityNote = Field(default='', exclude=True)


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

## Register entities
# Helper class to wrap the entity class and its type
class EntityWrapper:
    def __init__(self, entity_class: Type[BaseEntity]):
        self.entity_class = entity_class
        self.entity_type = entity_class.model_fields['setting'].default.type

    def get_cls(self) -> Type[BaseEntity]:
        return self.entity_class

    def get_type(self) -> Type[BaseEntity]:
        return self.entity_type
    def __repr__(self):
        return f"<EntityWrapper: {self.entity_type}>"

    def __str__(self):
        return self.name

# Define the metaclass to dynamically register the entities
class RegisterMeta(type):
    def __new__(cls, name, bases, class_dict):
        # Create the new class (like Register)
        new_cls = super().__new__(cls, name, bases, class_dict)

        # Initialize a registry to store entity information
        new_cls._entity_registry: Dict[str, EntityWrapper] = {}

        # Iterate through the class attributes and register any BaseModel subclasses
        for attr_name, attr_value in class_dict.items():
            if isinstance(attr_value, type) and issubclass(attr_value, BaseModel):
                # Register entity dynamically
                new_cls._entity_registry[attr_name] = EntityWrapper(entity_class=attr_value)
                # Also set it as an attribute of the class
                setattr(new_cls, attr_name, EntityWrapper(attr_value))

        return new_cls

    def get_cls(cls, name: str) -> Type[BaseEntity]:
        return cls._entity_registry.get(name).get_cls()

# Define the base class for the entity register

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
