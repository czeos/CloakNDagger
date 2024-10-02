from maltego_trx.transform import DiscoverableTransform
from maltego_trx.maltego import MaltegoTransform, MaltegoMsg

from extensions import registry
from settings import cloak_n_dagger_transformset
from tools.maltego import entity_from_model, model_from_maltego_request
from tools.entities import entity_register, CloakNDagger, Case, Alias, Tavily
from modules.cloak_n_dagger.gui import check_box_form


starting_entities = {'Hunchly Case': entity_register.get_type(Case),
                    'Whatsmyname App': entity_register.get_type(Alias),
                    'Tavily search': entity_register.get_type(Tavily)}

@registry.register_transform(
    display_name="Get CND strarting Entity [CloakNDagger]",
    input_entity=entity_register.get_type(CloakNDagger),
    description="Get starting entity",
    output_entities=[entity for entity in starting_entities.values()],
    transform_set=cloak_n_dagger_transformset

)
class CND_GetEntity(DiscoverableTransform):
    """
    Get a page dat from Hunchly Case
    """
    @classmethod
    def create_entities(cls, request: MaltegoMsg, response: MaltegoTransform):
        # build query
        _ = model_from_maltego_request(request=request, model=CloakNDagger)
        selected_entities = check_box_form(options=[name for name in starting_entities.keys()],
                                        title='CloakNDagger',
                                        description='Select main project entities')


        items = [starting_entities.get(name).get_cls()() for name in selected_entities]

        # generating of pages
        for item in items:
            entity_from_model(item, response)

        response.addUIMessage(f"{len(selected_entities)} were created")

