from maltego_trx.transform import DiscoverableTransform
from maltego_trx.maltego import MaltegoTransform, MaltegoMsg

from extensions import registry
from modules.hunchly.api import get_case_pages
from utils import create_entity_from_model


@registry.register_transform(
    display_name="Get Pages [Hunchly]",
    input_entity="cnd.HunchlyCase",
    description="Return captured pages for given Hunchly case name",
    output_entities=['cnd.HunchlyWebpage'],

)
class GetPages(DiscoverableTransform):
    """
    Get a pages from Hunchly Case
    """

    @classmethod
    def create_entities(cls, request: MaltegoMsg, response: MaltegoTransform):
        # how many
        howmany = request.Slider

        # TODO: implement slidebar

        # case data
        case_name = request.Value
        case = get_case_pages(case_name)

        # generating of pages
        for page in case.pages:
            create_entity_from_model(page, response)

        response.addUIMessage(f"Page contain {case.number_of_results} pages")


