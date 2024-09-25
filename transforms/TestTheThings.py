from maltego_trx.maltego import MaltegoTransform, MaltegoMsg
from maltego_trx.transform import DiscoverableTransform

from extensions import registry
from modules.ares.models import RequestEkonomickySubjekt
from settings import ares_transformset
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
        t = TestEntity(**output)
        t.set_display_info(content=None, title=None)
        t.set_note(note=None)
        t.set_icon(url=None)
        entity_from_model(model=t, response=response)


    @classmethod
    def run_transform(cls, request: MaltegoMsg):
        response = MaltegoTransform()
        for _ in range(5):  # Loop to call create_entities multiple times
            cls.create_entities(request, response)
        return response.returnOutput()

