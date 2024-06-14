from maltego_trx.transform import DiscoverableTransform
from maltego_trx.maltego import MaltegoTransform, MaltegoMsg

from extensions import registry
from settings import hunchly_transformset
from modules.hunchly.api import get_page_tags
from tools.base import ENTITIES_TYPE_NAMES
from tools.maltego import create_entity_from_model


@registry.register_transform(
    display_name="Get Page Tags [Hunchly]",
    input_entity=ENTITIES_TYPE_NAMES.PAGE,
    description="Return tags for given Hunchly Webpage",
    output_entities=[ENTITIES_TYPE_NAMES.TAG],
    transform_set=hunchly_transformset

)
class GetPageTags(DiscoverableTransform):
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
        results = get_page_tags(page_id)

        # generating of pages
        for item in results.data:
            create_entity_from_model(item, response)

        response.addUIMessage(f"Case contain {results.results} pages")