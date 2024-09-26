from maltego_trx.maltego import MaltegoTransform, MaltegoMsg
from maltego_trx.transform import DiscoverableTransform

from extensions import registry
from settings import ares_transformset
from tools.maltego import entity_from_model, model_from_maltego_request
from tools.entities import ENTITYREG, Company
from tools.base import MaltegoSettingAttributes
from modules.ares import ares_logger
from modules.ares.models import AresICO

@registry.register_transform(
    display_name="Extract ICO",
    input_entity=ENTITYREG.COMPANY.get_type(),
    description="Extract Company ICO",
    output_entities=[ENTITYREG.ICO.get_type()],
    transform_set=ares_transformset
)

class Ares_ExtractICO(DiscoverableTransform):
    """
    Extracts the address from the company entity
    """

    @classmethod
    def create_entities(cls, request: MaltegoMsg, response: MaltegoMsg):
        input_company = model_from_maltego_request(request, model=Company)
        dict_company = input_company.entity_dump(exclude=[MaltegoSettingAttributes])
        if not input_company:
            return
        entity_from_model(model=AresICO(**dict_company), response=response)
        