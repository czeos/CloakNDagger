from pydantic import Field


from tools.base import BaseEntity, EntitySetting, register_entity
from tools.entities import entity_register




@register_entity
class Adress2(BaseEntity):
    setting: EntitySetting = Field(default=EntitySetting(type='cnd.adress_entity1',
                                                         main_attribute='sidlo',
                                                         match='strict'))
    sidlo: str = Field(default='')

@register_entity
class ICO2(BaseEntity):
    setting: EntitySetting = Field(default=EntitySetting(type='cnd.ico_entity1',
                                                         main_attribute='ico',
                                                         match='strict'))
    ico: str = Field(default='')

# This class will not be registered as it doesn't inherit from BaseEntity
@register_entity
class UnrelatedClass:
    pass


entity_register.get_type(Adress2)
entity_register.get_type(ICO2)
