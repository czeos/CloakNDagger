from maltego_trx.transform import DiscoverableTransform
from maltego_trx.maltego import MaltegoTransform, MaltegoMsg

from extensions import registry
from settings import hunchly_transformset
from modules.hunchly.api import get_page_selectors
from tools.entities import entity_register, Page, Selector
from tools.maltego import entity_from_model


@registry.register_transform(
    display_name="Get Page Selectors [Hunchly]",
    input_entity=entity_register.get_type(Page),
    description="Return selectors for given Hunchly Webpage",
    output_entities=[entity_register.get_type(Selector)],
    transform_set=hunchly_transformset

)
class Hunchly_GetPageSelectors(DiscoverableTransform):
    """
    Get a pages from Hunchly Case
    """

    @classmethod
    def create_entities(cls, request: MaltegoMsg, response: MaltegoTransform):
        # how many
        howmany = request.Slider

        # TODO: implement slidebar

        # case data
        page_id = request.getProperty('id')
        results = get_page_selectors(page_id)

        # generating of pages
        for item in results.data:
            entity_from_model(item, response)

        response.addUIMessage(f"Case contain {results.results} selectors")