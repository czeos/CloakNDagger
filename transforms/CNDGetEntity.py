from maltego_trx.transform import DiscoverableTransform
from maltego_trx.maltego import MaltegoTransform, MaltegoMsg

from extensions import registry
from settings import cloak_n_dagger_transformset
from tools.maltego import create_entity_from_model, model_from_maltego_request
from tools.entities import ENTITIES_TYPE_NAMES, CloakNDagger, entity_register
from modules.cloak_n_dagger.gui import check_box_form


starting_entities = [ENTITIES_TYPE_NAMES.CASE,
                    ENTITIES_TYPE_NAMES.ALIAS,
                    ENTITIES_TYPE_NAMES.TAVILY]

@registry.register_transform(
    display_name="Get CND strarting Entity [CloakNDagger]",
    input_entity=ENTITIES_TYPE_NAMES.CLOAK_N_DAGGER,
    description="Get starting entity",
    output_entities=[name for name in starting_entities],
    transform_set=cloak_n_dagger_transformset

)
class CNDGetEntity(DiscoverableTransform):
    """
    Get a page dat from Hunchly Case
    """
    @classmethod
    def create_entities(cls, request: MaltegoMsg, response: MaltegoTransform):
        # build query
        _ = model_from_maltego_request(request=request, model=CloakNDagger)
        selected_entities = check_box_form(options=starting_entities,
                                        title='CloakNDagger',
                                        description='Select main project entities')


        items = [entity_register.get_item(name)() for name in selected_entities]

        # generating of pages
        for item in items:
            create_entity_from_model(item, response)

        response.addUIMessage(f"{len(selected_entities)} were created")


