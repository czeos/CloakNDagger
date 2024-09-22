from maltego_trx.maltego import MaltegoTransform, MaltegoMsg
from maltego_trx.transform import DiscoverableTransform

from extensions import registry
from modules.ares.models import RequestEkonomickySubjekt
from settings import ares_transformset
from tools.base import ENTITIES_TYPE_NAMES
from tools.maltego import model_from_maltego_request, entity_from_model
from tools.entities import Company, ENTITYREG, TestEntity

@registry.register_transform(
    display_name="TestTheThings",
    input_entity=ENTITYREG.COMPANY.get_type(),
    description="TestTheThings",
    output_entities=[ENTITYREG.TEST_ENTITY.get_type()],
    transform_set=ares_transformset
)
class TestTheThings(DiscoverableTransform):


    @classmethod
    def create_entities(cls, request: MaltegoMsg, response: MaltegoTransform):
        # build query
        input_company = model_from_maltego_request(request=request, model=Company)
        search_request = RequestEkonomickySubjekt(**input_company.model_dump())
        output = {
            "fullname": "Test"
        }

        entity_from_model(model=TestEntity(**output), response=response)




if __name__ == "__main__":
    from tools.entities import TestEntity
    from tools.maltego import entity_from_model
    from maltego_trx.maltego import MaltegoTransform, MaltegoMsg
    response = MaltegoTransform()
    output = {
        "fullname": "Test"
    }

    t = TestEntity(**output)
    entity_from_model(model=TestEntity(**output), response=response)
