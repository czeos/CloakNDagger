from maltego_trx.transform import DiscoverableTransform
from maltego_trx.maltego import MaltegoTransform, MaltegoMsg

from extensions import registry
from modules.hunchly.api import get_page_photo
from utils import create_entity_from_model


@registry.register_transform(
    display_name="Get Page Photos [Hunchly]",
    input_entity="cnd.HunchlyWebpage",
    description="Return photos for given Hunchly Webpage",
    output_entities=['maltego.Image'],

)
class GetPagePhoto(DiscoverableTransform):
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
        page = get_page_photo(page_id)

        # generating of pages
        for item in page.photos:
            create_entity_from_model(item, response)

        response.addUIMessage(f"Case contain {page.number_of_results} pages")


