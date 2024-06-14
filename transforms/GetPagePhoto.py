from maltego_trx.transform import DiscoverableTransform
from maltego_trx.maltego import MaltegoTransform, MaltegoMsg

from extensions import registry
from settings import hunchly_transformset
from modules.hunchly.api import get_page_photo
from tools.base import ENTITIES_TYPE_NAMES
from tools.maltego import create_entity_from_model


@registry.register_transform(
    display_name="Get Page HunchlyPhotos [Hunchly]",
    input_entity=ENTITIES_TYPE_NAMES.PAGE,
    description="Return photos for given Hunchly Webpage",
    output_entities=[ENTITIES_TYPE_NAMES.PHOTO],
    transform_set=hunchly_transformset

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
        for item in page.data:
            create_entity_from_model(item, response)

        response.addUIMessage(f"Case contain {page.results} pages")


