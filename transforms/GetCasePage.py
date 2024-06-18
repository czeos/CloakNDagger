from maltego_trx.transform import DiscoverableTransform
from maltego_trx.maltego import MaltegoTransform, MaltegoMsg

from extensions import registry
from modules.hunchly.models import Case
from settings import hunchly_transformset
from modules.hunchly.api import get_case_page, get_cases, get_case_pages_by_case_id
from modules.hunchly.gui import check_box_form
from tools.maltego import create_entity_from_model, model_from_maltego_request
from tools.entities import ENTITIES_TYPE_NAMES
from tools.gui.components import message_box

@registry.register_transform(
    display_name="Get HunchlyPage [Hunchly]",
    input_entity=ENTITIES_TYPE_NAMES.CASE,
    description="Return captured pages for given Hunchly case name",
    output_entities=[ENTITIES_TYPE_NAMES.PAGE],
    transform_set=hunchly_transformset

)
class GetCasePage(DiscoverableTransform):
    """
    Get a pages from Hunchly Case
    """

    @classmethod
    def create_entities(cls, request: MaltegoMsg, response: MaltegoTransform):
        # data prepration - entity should be empty or incomplete, thus case must be get from hunchly and compared
        # transform request to case
        request_case = model_from_maltego_request(request=request, model=Case)

        # get cases
        cases = get_cases()

        # prepare value to populate gui
        if request_case.name:
            case = cases.get_case_by_name(request_case.name)
            case_names, case_ids = [case.name], [case.id]
        elif request_case.id:
            case = cases.get_case_by_id(request_case.id)
            case_names, case_ids = [case.name], [case.id]
        else:
            case_names, case_ids = cases.get_list_of_item_values('name'), cases.get_list_of_item_values('id')

        output = check_box_form(title='Get page from case',
                                description='Select case and then select page by title or id. Id cn be found at '
                                            'Hunchly Dashboard ',
                                case_names=case_names,
                                case_ids=case_ids,
                                api_function=get_case_pages_by_case_id)

        if not output.id:
            message_box(message='Page doesnt found', title='CloakNDagger MessageBox', description='')
        else:
            items = get_case_page(str(output.id))
            for item in items.data:
                create_entity_from_model(item, response)
            message_box(message='Page created', title='CloakNDagger MessageBox', description='')

if  __name__ == "__main__":
    from tools.utils import DummyRequest
    request = DummyRequest(Value='')






    pass

