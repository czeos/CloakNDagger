from maltego_trx.transform import DiscoverableTransform
from maltego_trx.maltego import MaltegoTransform, MaltegoMsg

from extensions import registry
from settings import tavily_transformset
from tools.maltego import create_entity_from_model, model_from_maltego_request
from tools.base import ENTITIES_TYPE_NAMES, entity_register
from modules.tavily.models import Tavily
from modules.tavily.gui import request_form
from modules.tavily.api import tivaly_api, response_to_entities, SearchRequest


@registry.register_transform(
    display_name="Query web resources [Tavili]",
    input_entity=ENTITIES_TYPE_NAMES.TAVILY,
    description="Get starting entity",
    output_entities=[ENTITIES_TYPE_NAMES.PAGE, ENTITIES_TYPE_NAMES.PHOTO],
    transform_set=tavily_transformset

)
class TavilySearch(DiscoverableTransform):
    """
    Get a page dat from Hunchly Case
    """

    @classmethod
    def create_entities(cls, request: MaltegoMsg, response: MaltegoTransform):
        # build query
        searach_request = model_from_maltego_request(request=request, model=Tavily)
        updated_request = request_form(request=searach_request ,
                                       title='Taviliy',
                                       description='Search on web with Tavily')

        params = SearchRequest(**updated_request.dict())

        tavili_search = tivaly_api(updated_request)
        if not tavili_search:
            response.addUIMessage(f"No response from Tavili")
        else:
            entities = response_to_entities(tavili_search)
            for item in entities:
                create_entity_from_model(model=item, response=response)
