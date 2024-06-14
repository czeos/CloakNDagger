from maltego_trx.transform import DiscoverableTransform
from maltego_trx.maltego import MaltegoTransform, MaltegoMsg

from extensions import registry
from modules.hunchly.models import Case
from settings import hunchly_transformset
from modules.hunchly.api import get_case_photo
from tools.base import ENTITIES_TYPE_NAMES
from tools.maltego import create_entity_from_model, model_from_maltego_request


@registry.register_transform(
    display_name="Get Case HunchlyPhotos [Hunchly]",
    input_entity=ENTITIES_TYPE_NAMES.CASE,
    description="Return photos collected from pages for given Hunchly case name",
    output_entities=[ENTITIES_TYPE_NAMES.PHOTO],
    transform_set=hunchly_transformset

)
class GetCasePhoto(DiscoverableTransform):
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
            create_entity_from_model(item, response)

        response.addUIMessage(f"Case contain {items.results} pages")



