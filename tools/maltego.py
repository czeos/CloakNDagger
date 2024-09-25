from typing import Type, Any
from pydantic import BaseModel, Field
from maltego_trx.maltego import MaltegoMsg, MaltegoTransform, MaltegoEntity
from tools.base import BaseEntity, MaltegoSettingAttributes, EntityDisplay, EntityDisplayInfo, EntityIcon, EntityNote
from config import Config




def entity_from_model(model: BaseEntity, response: MaltegoTransform) -> MaltegoEntity:
    #create entity and set main attribute, type and matching rule based on the EntitySetting
    entity = response.addEntity(model.setting.type, model.__getattribute__(model.setting.main_attribute))

    for attr, field in model.__dict__.items():
        if not field:
            continue
        if not isinstance(field, MaltegoSettingAttributes):
            #add property to entity if not type of MaltegoSettingAttributes
            entity.addProperty(fieldName=attr, matchingRule=model.setting.match, value=field)
        if isinstance(field, EntityIcon):
            entity.setIconURL(field.url)
        if isinstance(field, EntityDisplayInfo):
            entity.addDisplayInformation(content=field.content, title=field.title)
        if isinstance(field, EntityDisplay):
            entity.addOverlay(propertyName=field.value, position=field.position, overlayType=field.overlay_type)
        if isinstance(field, EntityNote):
            entity.setNote(field.note)
    return entity



def create_entity_from_model(model: BaseEntity, response: MaltegoTransform) -> MaltegoEntity:
    entity = response.addEntity(model.setting.type, model.__getattribute__(model.setting.main_attribute))
    for field in model.property_fields:
        entity.addProperty(fieldName=field, matchingRule=model.setting.match, value=model.__getattribute__(field))
    if model.icon:
        entity.setIconURL(model.icon)
    if model.display_info:
        entity.addDisplayInformation(content=model.display_info)
        entity.addOverlay()
    return entity



def model_from_maltego_request(request: MaltegoMsg, model: Type[BaseEntity]) -> BaseEntity:
    """
    Automatic population of the model from maltego MSG
    """
    items = {key: value for key, value in request.Properties.items()}
    items[model.model_fields['setting'].default.main_attribute] = request.Value
    return model.model_validate(items)


class Slider(BaseModel):
    conf: Config
    request: Any

    @property
    def count(self) -> int:
        if self.conf.cnd.community:
            return 12
        else:
            return self.request.Slider