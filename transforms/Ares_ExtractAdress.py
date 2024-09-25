from maltego_trx.maltego import MaltegoTransform, MaltegoMsg
from maltego_trx.transform import DiscoverableTransform

from extensions import registry
from settings import ares_transformset
from tools.maltego import entity_from_model, model_from_maltego_request
from tools.entities import ENTITYREG, Adress, Company
from tools.base import MaltegoSettingAttributes
from modules.ares import ares_logger

@registry.register_transform(
    display_name="Extract Adress",
    input_entity=ENTITYREG.COMPANY.get_type(),
    description="Extract Company Adress",
    output_entities=[ENTITYREG.ADRESS.get_type()],
    transform_set=ares_transformset
)

class Ares_ExtractAdress(DiscoverableTransform):
    """
    Extracts the address from the company entity
    """

    @classmethod
    def create_entities(cls, request: MaltegoMsg, response: MaltegoMsg):
        input_company = model_from_maltego_request(request, model=Company)
        dict_company = input_company.entity_dump(exclude=[MaltegoSettingAttributes])
        if not input_company:
            return
        entity_from_model(model=Adress(**dict_company), response=response)
        