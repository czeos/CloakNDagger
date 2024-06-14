from maltego_trx.transform import DiscoverableTransform
from maltego_trx.maltego import MaltegoTransform, MaltegoMsg

from extensions import registry
from settings import hunchly_transformset
from modules.hunchly.api import get_cases
from modules.hunchly.models import Case
from tools.maltego import create_entity_from_model, model_from_maltego_request
from tools.entities import ENTITIES_TYPE_NAMES

@registry.register_transform(
    display_name="Get Hunchly Cases [Hunchly]",
    input_entity=ENTITIES_TYPE_NAMES.CASE,
    description="Return Hunchly Cases if no case name or id is provided",
    output_entities=[ENTITIES_TYPE_NAMES.CASE],
    transform_set=hunchly_transformset

)
class GetCases(DiscoverableTransform):
    """
    Return cases for empty case entity
    """

    @classmethod
    def create_entities(cls, request: MaltegoMsg, response: MaltegoTransform):
        # how many
        howmany = request.Slider
        # TODO: implement slidebar

        # case data

        case = model_from_maltego_request(request=request, model=Case)

        items = get_cases(case.name)

        # lookup
        case_names = [item.name for item in items.data]
        if case.name in case_names:
            i = case_names.index(case.name)
            item = items.data[i]
            create_entity_from_model(item, response)
        elif case.name not in case_names and not case.name in ['', ' ']:
            response.addUIMessage(f"Case name: {case.name}  did not find")
        else:
            for item in items.data:
                create_entity_from_model(item, response)



