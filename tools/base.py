from abc import ABC
from functools import wraps
from typing import Callable, Union, Dict, List, Type, Literal, Protocol, Optional, Any
from pydantic import BaseModel, Field, ConfigDict, field_serializer


from tools.utils import hash_fn
from enum import Enum
from maltego_trx.overlays import OverlayPosition, OverlayType


class EntityStackProtocol(Protocol):
    results: int
    data: list[BaseModel]


class BaseEntityProtocol(Protocol):

    setting: BaseModel
    uuid: str
    icon: str | BaseModel
    display_info: str | BaseModel
    note: str | BaseModel

    @property
    def property_fields(self) -> List[str]:
        ...

    def __hash__(self) -> int:
        ...


class MaltegoSettingAttributes(BaseModel):
    """
    Base type to set dynamically distinguish trough type check which fields will be set as entity properties and which
    are entity settings
    """
    def __bool__(self):
        return any(self.__getattribute__(attr) is not None for attr in self.__dict__.keys())

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
    """
    Class  representing matlego entity display settings. It can be used to set the entity overlay type, position and value
    """
    value: str | None
    position: OverlayPosition | None
    overlay_type: OverlayType | None

    @field_serializer('position', 'overlay_type')
    def serilize_enum(self, value):
        return value.value



class EntityIcon(MaltegoSettingAttributes):
    url: str | None = Field(default=None)


class EntityNote(MaltegoSettingAttributes):
    note: str | None = Field(default=None)


class EntityDisplayInfo(MaltegoSettingAttributes):
    content: str | None = Field(default=None)
    title: str | None = Field(default=None)


class BaseEntity(BaseModel):
    """
    Base entity / inheritance and template type

    """
    setting: EntitySetting = Field(...)
    icon: EntityIcon = Field(default_factory=EntityIcon)
    display_info: EntityDisplayInfo = Field(default_factory=EntityDisplayInfo)
    note: EntityNote = Field(default_factory=EntityNote)

    model_config = ConfigDict(extra='allow', arbitrary_types_allowed=True)

    @property
    def property_fields(self) -> List[str]:
        """
        Return list of attributes that will be map on the entity properties
        """
        return [attr for attr in self.entity_dump(exclude=[MaltegoSettingAttributes]).keys()]

    def __hash__(self):
        return hash_fn(self.model_dump())

    def set_icon(self, url: str | None) -> None:
        self.icon = EntityIcon(url=url)

    def set_note(self, note: str):
        self.note = EntityNote(note=note)

    def set_display_info(self, content: str, title: str):
        self.display_info = EntityDisplayInfo(content=content, title=title)

    def set_overlay(self, attr_name: str, value: str, position: Enum, overlay_type: Enum):
        """
        Set an overlay attribute for the entity.

        Parameters:
        attr_name (str): The name of the attribute to set the overlay on.
        value (str): The value to set for the overlay.
        position (Enum): The position of the overlay.
        overlay_type (Enum): The type of the overlay.
        """
        # define overlay
        overlay = EntityDisplay(value=value, position=position, overlay_type=overlay_type)
        # set overlay as attribute
        setattr(self, attr_name, overlay)

    def entity_dump(self, exclude: Optional[List[Union[str, Type[MaltegoSettingAttributes]]]] = []) -> dict:
        """
        Method will dump entity properties to dict. Method will exclude all attributes that are specified in exclude parameter
        by attr name or type or subtype.
        """
        # Prepare the exclusion set. Set takes as base all attributes defined as string or empty se
        exclude_set = set([name for name in exclude if isinstance(name, str)] or [])
        #list type exlude
        exclude_types = [ex_type for ex_type in exclude if isinstance(ex_type, type)]

        # get remaining attributes to map
        attrs_set = {name for name in self.__dict__.keys()}.difference(exclude_set)

        for attr_name in attrs_set:
            if any(isinstance(self.__getattribute__(attr_name), ex_type) for ex_type in exclude_types):
                exclude_set.add(attr_name)

        # Use Pydantic's model_dump method with the exclude parameter
        return self.model_dump(exclude=exclude_set)


class Cacheble(Protocol):

    def __hash__(self):
        ...

    def entity_dump(self, exclude: Optional[List[Union[str, Type[MaltegoSettingAttributes]]]] = []) -> dict:
        ...


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

    def get_type(self) -> str:
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
                wrapper = EntityWrapper(entity_class=attr_value)
                new_cls._entity_registry[wrapper.entity_type] = wrapper
                # Also set it as an attribute of the class
                setattr(new_cls, attr_name, EntityWrapper(attr_value))

        return new_cls

    # def get_cls(self, name: str) -> Type[BaseEntity]:
    #     wrapper = self._entity_registry.get(name)
    #     if wrapper:
    #         return wrapper.get_cls()
    #     raise AttributeError(f"Entity class '{name}' not found in registry.")
    #
    # def get_type(self, cls: Type[BaseEntity]) -> str:
    #     if issubclass(cls, BaseEntity):
    #         type_name = cls.model_fields['setting'].default.type
    #     else:
    #         raise TypeError(f"Input class in not subtype of BaseEntity")
    #
    #     if type_name in self._entity_registry.keys():
    #         wrapper = self._entity_registry.get(type_name)
    #         return wrapper.get_type()
    #     else:
    #         raise AttributeError(f"Entity class '{type_name}' not found in registry.")

    def __call__(self, *args, **kwargs):
        return self



class RegisterProtocol(Protocol):

    def get_cls(cls, name: str) -> Type[BaseEntity]:
        ...

# Define the base class for the entity register
class Register(metaclass=RegisterMeta):
    """
    All entities are registered here
    Entities are registered dynamically and wrapped in EntityWrapper
    attributes:
        clas: class of entity
        name: type of entity i.e. return value of entity.setting.type
    """

    @classmethod
    def get_cls(cls, name: str) -> Type[BaseEntity]:
        wrapper = cls._entity_registry.get(name)
        if wrapper:
            return wrapper.get_cls()
        raise AttributeError(f"Entity class '{name}' not found in registry.")

    @classmethod
    def get_type(cls, entity_cls: Type[BaseEntity]) -> str:
        if issubclass(entity_cls, BaseEntity):
            type_name = entity_cls.model_fields['setting'].default.type
        else:
            raise TypeError(f"Input class in not subtype of BaseEntity")

        if type_name in cls._entity_registry.keys():
            wrapper = cls._entity_registry.get(type_name)
            return wrapper.get_type()
        else:
            raise AttributeError(f"Entity class '{type_name}' not found in registry.")


def register_entity(cls):
    if issubclass(cls, BaseEntity):
        wrapper_instance = EntityWrapper(entity_class=cls)
        entity_type = wrapper_instance.entity_type
        if entity_type in Register._entity_registry.keys():
            raise AttributeError(f"Entity type name '{entity_type}' for class {cls.__name__} already registered.")
        Register._entity_registry[entity_type] = wrapper_instance
        setattr(Register, cls.__name__, wrapper_instance)
    return cls