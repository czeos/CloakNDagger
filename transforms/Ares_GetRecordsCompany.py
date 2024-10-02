from typing import List
from maltego_trx.maltego import MaltegoTransform, MaltegoMsg
from maltego_trx.transform import DiscoverableTransform

from config import config
from extensions import registry
from modules.ares.gui import show_form
from modules.ares.models import RequestEkonomickySubjekt, RequestFormEkonomickySubjekt
from settings import ares_transformset
from tools.dbs import TiDBCache
from tools.maltego import model_from_maltego_request, entity_from_model
from modules.ares.api import serch_ares
from tools.entities import Company, Person, ENTITYREG
from tools.gui import create_dynamic_form, create_message_box
from modules.ares import ares_logger

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
        # how many
        howmany = request.Slider
        howmany = 12
        # build query
        ares_logger.debug('Start Ares_GetRecordsCompany')
        input_company = model_from_maltego_request(request=request, model=Company)

        #transform input to form attributes
        form = RequestFormEkonomickySubjekt(**input_company.model_dump())

        # invoke formular
        ares_logger.debug('Invoke  modal form')
        form = create_dynamic_form(model_class=RequestFormEkonomickySubjekt,
                                   init_values=form.model_dump(),
                                   title='Ares search',
                                   description='Fill the form to search in ARES',
                                   default_fields=['obchodniJmeno'],
                                   exclude_fields=['pocet', 'start'])

        #transform form to request format
        search_request = RequestEkonomickySubjekt(**form.model_dump())


        if search_request:


            companies = serch_ares(search_request)

            if not companies:
                create_message_box(message=f"No response from ARES", title='CloakNDagger MessageBox', description='')

            else:
                for company in companies.ekonomickeSubjekty:
                    entity_from_model(model=company, response=response)



if __name__ == "__main__":
    from tools.utils import DummyRequest

    input_company = Company(name='Google Inc.', ico='12345678', address='Jankovcova 1522/53, Holešovice, 17000 Praha 7')

    form = RequestFormEkonomickySubjekt(**input_company.model_dump())

    # invoke formular
    ares_logger.debug('Invoke  modal form')
    form = create_dynamic_form(model_class=RequestFormEkonomickySubjekt,
                               init_values=form.model_dump(),
                               title='Ares search',
                               description='Fill the form to search in ARES',
                               default_fields=['obchodniJmeno'],
                               exclude_fields=['pocet', 'start'])

    search = RequestEkonomickySubjekt(**form.model_dump())

    ares_logger.debug('Test if data is filled')
    if search_request:
        #cache
        cache = TiDBCache(db_path=config.db.db_path)

        if cache.query_cache_size(query=search) > 0:
            #cached routine
            cached_stack = cache.get_records(query=username, count=howmany)
            entities = db_records_to_entity(register=ENTITYREG, stack=cached_stack)
            items = UserProfiles(results=cache.query_cache_size(username), data=entities)

        else:
            # get data from site
            wmnd = get_site_dat(config.whatsmynmeapp.data)
            profiles = check_all_sites(wmnd.sites, username.alias, HEADERS)
            if len(profiles) > howmany:
                cache.save_to_cache(query=username, entities=profiles[howmany:])
            items = UserProfiles(results=len(profiles), data=profiles[:howmany])




        ares_logger.debug('Call ARES')
        companies = serch_ares(search_request)

        if not companies:
            create_message_box(message=f"No response from ARES", title='CloakNDagger MessageBox', description='')

        else:
            for company in companies.ekonomickeSubjekty:
                entity_from_model(model=company, response=response)



