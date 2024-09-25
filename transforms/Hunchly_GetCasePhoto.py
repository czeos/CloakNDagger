from maltego_trx.transform import DiscoverableTransform
from maltego_trx.maltego import MaltegoTransform, MaltegoMsg

from extensions import registry
from modules.hunchly.models import Case
from settings import hunchly_transformset
from modules.hunchly.api import get_case_photo
from tools.entities import ENTITYREG
from tools.maltego import entity_from_model, model_from_maltego_request


@registry.register_transform(
    display_name="Get Case Photos [Hunchly]",
    input_entity=ENTITYREG.CASE.get_type(),
    description="Return photos collected from pages for given Hunchly case name",
    output_entities=[ENTITYREG.PHOTO.get_type()],
    transform_set=hunchly_transformset

)
class Hunchly_GetCasePhoto(DiscoverableTransform):
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
        items = get_case_photo(case.name)

        # generating of pages
        for item in items.data:
            entity_from_model(item, response)

        response.addUIMessage(f"Case contain {items.results} pages")



