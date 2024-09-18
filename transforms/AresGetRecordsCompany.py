from maltego_trx.maltego import MaltegoTransform, MaltegoMsg
from maltego_trx.transform import DiscoverableTransform

from extensions import registry
from settings import ares_transformset
from tools.base import ENTITIES_TYPE_NAMES
from tools.maltego import model_from_maltego_request, create_entity_from_model
from modules.ares.models import Company
from modules.ares.api import serch_by_name


@registry.register_transform(
    display_name="Get legal info from ARES",
    input_entity=ENTITIES_TYPE_NAMES.COMPANY,
    description="Get legal info from ARES (CZE) for given company name",
    output_entities=[ENTITIES_TYPE_NAMES.COMPANY],
    transform_set=ares_transformset

)
class AresGetRecordsCompany(DiscoverableTransform):


    @classmethod
    def create_entities(cls, request: MaltegoMsg, response: MaltegoTransform):
        # build query
        search_request = model_from_maltego_request(request=request, model=Company)

        company = serch_by_name(search_request.name)
        create_entity_from_model(model=company, response=response)




