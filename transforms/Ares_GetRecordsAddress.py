from typing import List
from maltego_trx.maltego import MaltegoTransform, MaltegoMsg
from maltego_trx.transform import DiscoverableTransform
from pydantic import BaseModel, Field

from extensions import registry
from modules.ares.gui import show_form
from modules.ares.models import RequestEkonomickySubjekt,Sidlo
from settings import ares_transformset
from tools.maltego import model_from_maltego_request, entity_from_model
from modules.ares.api import serch_ares
from tools.entities import Adress, Company, Person, ENTITYREG

@registry.register_transform(
    display_name="Get ARES info from address",
    input_entity=ENTITYREG.ADRESS.get_type(),
    description="Get legal info from ARES (CZE) for given address",
    output_entities=[ENTITYREG.COMPANY.get_type(), ENTITYREG.PERSON.get_type()],
    transform_set=ares_transformset

)

class Ares_GetRecordsAddress(DiscoverableTransform):


    @classmethod
    def create_entities(cls, request: MaltegoMsg, response: MaltegoTransform):
        # build query
        
        input_address = model_from_maltego_request(request=request, model=Adress)
        search_request = RequestEkonomickySubjekt(sidlo=Sidlo(textovaAdresa=input_address.sidlo))
        
        data = show_form({'adress': search_request.sidlo.textovaAdresa})
        if data:
            search_request.ico = [data.ico] if data.ico else None
            search_request.obchodniJmeno = data.name if data.name else None 

            response.addUIMessage(search_request)
            companies = serch_ares(search_request)

            if not companies:
                response.addUIMessage(f"No response from ARES")
            else:
                for company in companies.ekonomickeSubjekty:
                    entity_from_model(model=company, response=response)




