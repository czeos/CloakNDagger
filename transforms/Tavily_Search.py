from maltego_trx.transform import DiscoverableTransform
from maltego_trx.maltego import MaltegoTransform, MaltegoMsg

from config import config
from extensions import registry
from settings import tavily_transformset
from tools.maltego import entity_from_model, model_from_maltego_request
from tools.entities import entity_register, Tavily, Page, Photo
from tools.base import MaltegoSettingAttributes
from modules.tavily.gui import request_form
from modules.tavily.api import tivaly_api, response_to_entities, SearchRequest

#TODO: Check for internet connection

@registry.register_transform(
    display_name="Query web resources [Tavili]",
    input_entity=entity_register.get_type(Tavily),
    description="Get starting entity",
    output_entities=[entity_register.get_type(Page), entity_register.get_type(Photo)],
    transform_set=tavily_transformset

)
class Tavily_Search(DiscoverableTransform):
    """
    Get a page dat from Hunchly Case
    """

    @classmethod
    def create_entities(cls, request: MaltegoMsg, response: MaltegoTransform):
        # build query
        tavili = model_from_maltego_request(request=request, model=Tavily)
        request =  SearchRequest(**tavili.entity_dump(exclude=[MaltegoSettingAttributes]),
                                 api_key=config.tavily.api_key)
        updated_request = request_form(request=request,
                                       title='Taviliy',
                                       description='Search on web with Tavily')

        tavili_search = tivaly_api(updated_request)
        if not tavili_search:
            response.addUIMessage(f"No response from Tavili")
        else:
            entities = response_to_entities(tavili_search)
            for item in entities:
                entity_from_model(model=item, response=response)
