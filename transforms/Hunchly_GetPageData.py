from maltego_trx.transform import DiscoverableTransform
from maltego_trx.maltego import MaltegoTransform, MaltegoMsg

from extensions import registry
from settings import hunchly_transformset
from modules.hunchly.api import get_page_data
from tools.entities import entity_register, Page, Email, IPV4, IPV6, GoogleAnalytics, FacebookPixel, TorService, SocialMediaProfile
from tools.maltego import entity_from_model


@registry.register_transform(
    display_name="Get Page Data [Hunchly]",
    input_entity=entity_register.get_type(Page),
    description="Return pages data for given Hunchly Webpage",
    output_entities=[entity_register.get_type(Email), entity_register.get_type(IPV4), entity_register.get_type(IPV6),
                      entity_register.get_type(GoogleAnalytics), entity_register.get_type(FacebookPixel),
                      entity_register.get_type(TorService), entity_register.get_type(SocialMediaProfile)],
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


