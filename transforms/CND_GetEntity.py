from maltego_trx.transform import DiscoverableTransform
from maltego_trx.maltego import MaltegoTransform, MaltegoMsg

from extensions import registry
from settings import cloak_n_dagger_transformset
from tools.maltego import create_entity_from_model, model_from_maltego_request
from tools.entities import ENTITYREG, CloakNDagger
from modules.cloak_n_dagger.gui import check_box_form


starting_entities = [ENTITYREG.CASE.get_type(),
                    ENTITYREG.ALIAS.get_type(),
                    ENTITYREG.TAVILY.get_type()]

@registry.register_transform(
    display_name="Get CND strarting Entity [CloakNDagger]",
    input_entity=ENTITYREG.CLOAK_N_DAGGER.get_type(),
    description="Get starting entity",
    output_entities=[name for name in starting_entities],
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
        selected_entities = check_box_form(options=starting_entities,
                                        title='CloakNDagger',
                                        description='Select main project entities')


        items = [ENTITYREG.get_cls(name)() for name in selected_entities]

        # generating of pages
        for item in items:
            create_entity_from_model(item, response)

        response.addUIMessage(f"{len(selected_entities)} were created")


