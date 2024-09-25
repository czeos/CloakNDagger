from maltego_trx.transform import DiscoverableTransform
from maltego_trx.maltego import MaltegoTransform, MaltegoMsg

from extensions import registry
from settings import hunchly_transformset
from modules.hunchly.api import get_page_data
from tools.entities import ENTITYREG
from tools.maltego import entity_from_model


@registry.register_transform(
    display_name="Get Page Data [Hunchly]",
    input_entity=ENTITYREG.PAGE.get_type(),
    description="Return pages data for given Hunchly Webpage",
    output_entities=[ENTITYREG.EMAIL.get_type(),
                     ENTITYREG.IPV4.get_type(),
                     ENTITYREG.IPV6.get_type(),
                     ENTITYREG.GOOGLE_ANALYTICS.get_type(),
                     ENTITYREG.FACEBOOK_PIXEL.get_type(),
                     ENTITYREG.TOR_SERVICE.get_type(),
                     ENTITYREG.SOCIAL_MEDIA_ACCOUNT.get_type()],
    transform_set=hunchly_transformset

)
class Hunchly_GetPageData(DiscoverableTransform):
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
        page = get_page_data(page_id)

        # generating of pages
        for item in page.data:
            entity_from_model(item, response)

        response.addUIMessage(f"Case contain {page.results} records")


