from maltego_trx.transform import DiscoverableTransform
from maltego_trx.maltego import MaltegoTransform, MaltegoMsg

from extensions import registry
from settings import hunchly_transformset
from modules.hunchly.api import get_page_photo
from tools.entities import ENTITYREG
from tools.maltego import entity_from_model


@registry.register_transform(
    display_name="Get Page Photos [Hunchly]",
    input_entity=ENTITYREG.PAGE.get_type(),
    description="Return photos for given Hunchly Webpage",
    output_entities=[ENTITYREG.PHOTO.get_type()],
    transform_set=hunchly_transformset

)
class Hunchly_GetPagePhoto(DiscoverableTransform):
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
            entity_from_model(item, response)

        response.addUIMessage(f"Case contain {page.results} photos")


