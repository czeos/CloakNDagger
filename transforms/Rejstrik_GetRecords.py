from maltego_trx.maltego import MaltegoTransform, MaltegoMsg
from maltego_trx.transform import DiscoverableTransform


from extensions import registry
from modules.rejstrik.api import find_relations
from modules.rejstrik.helper_methods import edges_to_entities
from settings import ares_transformset
from tools.maltego import entity_from_model, model_from_maltego_request
from tools.entities import entity_register, Company, Person
from tools.base import EntityDisplay, MaltegoSettingAttributes
from modules.ares import ares_logger
from modules.ares.models import AresICO

@registry.register_transform(
    display_name="Rejstrik Get Records",
    input_entity=entity_register.get_type(Company),
    description="Extract information about the company from Rejstrik",
    output_entities=[entity_register.get_type(Company), entity_register.get_type(Person)],
    transform_set=ares_transformset
)

class Rejstrik_GetRecords(DiscoverableTransform):


    @classmethod
    def create_entities(cls, request: MaltegoMsg, response: MaltegoMsg):
        input_company = model_from_maltego_request(request, model=Company)
        dict_company = input_company.entity_dump(exclude=[MaltegoSettingAttributes])

        if not input_company:
            return

        if 'ico' not in dict_company:
            response.addUIMessage(f"Entita neobsahuje atribut IČO")
            return

        ic = dict_company['ico']
        resp = find_relations(ico=ic)

        item = next((x for x in resp.nodes if x.data.ico == ic), None)
        dict_node = {node.data.id: node.data for node in resp.nodes}

        for edge in resp.edges:
            if item.data.id == edge.data.target:
                data = edges_to_entities(item,dict_node[edge.data.source],edge)
                e = entity_from_model(model=data, response=response)
                e.reverseLink()
            elif item.data.id == edge.data.source:
                data = edges_to_entities(item,dict_node[edge.data.target],edge)
                entity_from_model(model=data, response=response)



        