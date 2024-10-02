from maltego_trx.transform import DiscoverableTransform
from maltego_trx.maltego import MaltegoTransform, MaltegoMsg
from pydantic import ValidationError

from extensions import registry
from settings import hunchly_transformset
from modules.hunchly.api import get_case_data, get_cases
from modules.hunchly.models import Case, HUNCHLY_DATA_TYPES
from tools.maltego import entity_from_model, model_from_maltego_request
from tools.gui.components import MultiSelectorMenu, message_box
from tools.entities import entity_register, Case, Email, IPV4, IPV6, GoogleAnalytics, FacebookPixel, TorService, SocialMediaProfile

HUNCHLY_DATA = []


@registry.register_transform(
    display_name="Get Case Data [Hunchly]",
    input_entity=entity_register.get_type(Case),
    description="Return data collected from pages for given Hunchly case name or case id",
    output_entities=[entity_register.get_type(Email), entity_register.get_type(IPV4), entity_register.get_type(IPV6),
                     entity_register.get_type(GoogleAnalytics), entity_register.get_type(FacebookPixel),
                     entity_register.get_type(TorService), entity_register.get_type(SocialMediaProfile)],
    transform_set=hunchly_transformset

)
class Hunchly_GetCaseData(DiscoverableTransform):
    """
    Get a page dat from Hunchly Case
    """

    @classmethod
    def create_entities(cls, request: MaltegoMsg, response: MaltegoTransform):
        # how many
        howmany = request.Slider

        # TODO: implement slidebar
        # TODO: add error for missing case name
        # case data
        response.addUIMessage(f"{request.Properties} /n {request.Type} ")

        case = model_from_maltego_request(request=request, model=Case)

        # get data
        try:
            items = get_case_data(case.name)
        except ValidationError as e:
            cases = get_cases()
            case_names = [item.name for item in cases.data]
            if case.name not in case_names:
                response.addException(f'Case name {case.name} does not exist')
            else:
                raise e

        # interactive GUI
        interactive = request.getProperty('interactive')

        if interactive == 'true':
            options = [name for name in HUNCHLY_DATA_TYPES.keys()]
            label ='Select Hunchly data type that will be returned'
            with MultiSelectorMenu(options, label) as app:
                app.root.mainloop()
                selected_option = app.get_selected_values()
            items.filter_by_types([HUNCHLY_DATA_TYPES.get(typ) for typ in selected_option], inplace=True)



        # generating of pages
        for item in items.data:
            entity_from_model(item, response)

        message_box(message=f"Case contain {items.results} items", title='CloakNDagger MessageBox', description='')
        response.addUIMessage(f"Case contain {items.results} items")



