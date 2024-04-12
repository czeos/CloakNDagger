from maltego_trx.transform import DiscoverableTransform
from maltego_trx.maltego import MaltegoTransform, MaltegoMsg

from extensions import registry
from modules.hunchly.api import get_case_selectors
from utils import create_entity_from_model


@registry.register_transform(
    display_name="Get Case Selectors [Hunchly]",
    input_entity="cnd.HunchlyCase",
    description="Return selectors collected from pages for given Hunchly case name",
    output_entities=['cnd.HunchlySelector'],

)
class GetCaseSelectors(DiscoverableTransform):
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
        case = get_case_selectors(case_name)

        # generating of pages
        for item in case.data:
            create_entity_from_model(item, response)

        response.addUIMessage(f"Case contain {case.number_of_results} pages")

