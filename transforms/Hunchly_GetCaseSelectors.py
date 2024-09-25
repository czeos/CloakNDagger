from maltego_trx.transform import DiscoverableTransform
from maltego_trx.maltego import MaltegoTransform, MaltegoMsg

from extensions import registry
from modules.hunchly.models import Case
from settings import hunchly_transformset
from modules.hunchly.api import get_case_selectors_by_case_name
from tools.entities import ENTITYREG
from tools.maltego import entity_from_model, model_from_maltego_request


@registry.register_transform(
    display_name="Get Case Selectors [Hunchly]",
    input_entity=ENTITYREG.CASE.get_type(),
    description="Return selectors collected from pages for given Hunchly case name",
    output_entities=[ENTITYREG.SELECTOR.get_type()],
    transform_set=hunchly_transformset

)
class Hunchly_GetCaseSelectors(DiscoverableTransform):
    """
    Get a pages from Hunchly Case
    """

    @classmethod
    def create_entities(cls, request: MaltegoMsg, response: MaltegoTransform):
        # how many
        howmany = request.Slider

        # TODO: implement slidebar

        # case data
        case = model_from_maltego_request(request=request, model=Case)
        items = get_case_selectors_by_case_name(case.name)

        # generating of pages
        for item in items.data:
            entity_from_model(item, response)

        response.addUIMessage(f"Case contain {items.results} selectors")

