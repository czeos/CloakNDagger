from typing import List
from maltego_trx.maltego import MaltegoTransform, MaltegoMsg
from maltego_trx.transform import DiscoverableTransform

from extensions import registry
from modules.ares.gui import show_form
from modules.ares.models import RequestEkonomickySubjekt,Sidlo
from settings import ares_transformset
from tools.maltego import model_from_maltego_request, entity_from_model
from modules.ares.api import serch_ares
from tools.entities import Company, Person, ENTITYREG

@registry.register_transform(
    display_name="Get legal info from ARES",
    input_entity=ENTITYREG.COMPANY.get_type(),
    description="Get legal info from ARES (CZE) for given company name",
    output_entities=[ENTITYREG.COMPANY.get_type(), ENTITYREG.PERSON.get_type()],
    transform_set=ares_transformset

)
class Ares_GetRecordsCompany(DiscoverableTransform):


    @classmethod
    def create_entities(cls, request: MaltegoMsg, response: MaltegoTransform):
        # build query
        
        input_company = model_from_maltego_request(request=request, model=Company)
        search_request = RequestEkonomickySubjekt(**input_company.model_dump())
        data = show_form({'name': search_request.obchodniJmeno})

        if data:
            search_request.ico = [data.ico] if data.ico else None
            search_request.sidlo = Sidlo(textovaAdresa=data.sidlo) if data.sidlo else None 

            response.addUIMessage(search_request)
            companies = serch_ares(search_request)

            if not companies:
                response.addUIMessage(f"No response from ARES")
            else:
                for company in companies.ekonomickeSubjekty:
                    entity_from_model(model=company, response=response)




