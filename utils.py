from maltego_trx.maltego import MaltegoTransform, MaltegoEntity

from base import BaseEntity

def create_entity_from_model(model: BaseEntity, response: MaltegoTransform) -> MaltegoEntity:
    entity = response.addEntity(model._entity_type, model.__getattribute__(model._entity_attr))
    for field in model.additional_fields:
        entity.addProperty(fieldName=field, matchingRule=model._entity_match_type, value=model.__getattribute__(field))
    return entity