from typing import List
from maltego_trx.maltego import MaltegoTransform, MaltegoMsg
from maltego_trx.transform import DiscoverableTransform

from config import config
from extensions import registry
from modules.ares.models import RequestEkonomickySubjekt, RequestFormEkonomickySubjekt, ResponseRoot
from settings import ares_transformset
from tools.dbs import TiDBCache, db_records_to_entity
from tools.maltego import model_from_maltego_request, entity_from_model
from modules.ares.api import serch_ares
from modules.ares.models import PravnickaOsoba, FyzickaOsoba
from tools.entities import Company, entity_register
from tools.gui import create_dynamic_form, create_message_box
from modules.ares import ares_logger

@registry.register_transform(
    display_name="Get legal info from ARES",
    input_entity=entity_register.get_type(Company),
    description="Get legal info from ARES (CZE) for given company name",
    # output_entities=[entity_register.get_type(PravnickaOsoba), entity_register.get_type(FyzickaOsoba)],
    output_entities=[entity_register.get_type(PravnickaOsoba), entity_register.get_type(FyzickaOsoba)],
    transform_set=ares_transformset

)

class Ares_GetRecordsCompany(DiscoverableTransform):

    @classmethod
    def create_entities(cls, request: MaltegoMsg, response: MaltegoTransform):
        # how many
        howmany = request.Slider
        howmany = 12
        # build query


        input_company = model_from_maltego_request(request=request, model=Company)

        #transform input to form attributes
        form = RequestFormEkonomickySubjekt(**input_company.model_dump())

        # invoke formular
        form = create_dynamic_form(model_class=RequestFormEkonomickySubjekt,
                                   init_values=form.model_dump(),
                                   title='Ares search',
                                   description='Fill the form to search in ARES',
                                   default_fields=[name for name in
                                                   form.model_dump(exclude_none=True, exclude_unset=True,
                                                                   exclude_defaults=True).keys()])

        #transform form to request format
        search = RequestEkonomickySubjekt(**form.model_dump())


        cache = TiDBCache(db_path=config.db.db_path)
        # cache using form as query because of user input

        if cache.query_cache_size(query=form) > 0:
            # cached routine
            cached_stack = cache.get_records(query=form, count=howmany)
            entities = db_records_to_entity(register=entity_register, stack=cached_stack)
            companies = ResponseRoot(pocetCelkem=len(entities), ekonomickeSubjekty=entities)

        else:
            # get data from site
            companies = serch_ares(search)

            if len(companies.ekonomickeSubjekty) > howmany:
                cache.save_to_cache(query=form, entities=companies.ekonomickeSubjekty[howmany:])
                companies = ResponseRoot(pocetCelkem=len(companies.ekonomickeSubjekty),
                                         ekonomickeSubjekty=companies.ekonomickeSubjekty[:howmany])


        if not companies:
            create_message_box(message=f"No response from ARES", title='CloakNDagger MessageBox',
                               description='')
        else:
            for company in companies.ekonomickeSubjekty:
                entity_from_model(model=company, response=response)

            in_cache = cache.query_cache_size(query=form)
            create_message_box(message=f"In cache left f'{in_cache}'", title='CloakNDagger MessageBox', description='')


if __name__ == "__main__":
    from tools.utils import DummyRequest

    # how many
    howmany = 12

    input_company = Company(address='Jankovcova 1522/53, Holešovice, 17000 Praha 7')

    # form = RequestFormEkonomickySubjekt(**input_company.model_dump())
    #
    # # invoke formular
    #
    # form = create_dynamic_form(model_class=RequestFormEkonomickySubjekt,
    #                            init_values=form.model_dump(),
    #                            title='Ares search',
    #                            description='Fill the form to search in ARES',
    #                            default_fields=[name for name in form.model_dump(exclude_none=True, exclude_unset=True, exclude_defaults=True).keys()])
    #
    # search = RequestEkonomickySubjekt(**form.model_dump())
    #
    # if search:
    #     # cache
    #     cache = TiDBCache(db_path=config.db.db_path)
    #     # cache using form as query because of user input
    #
    #     if cache.query_cache_size(query=form) > 0:
    #         # cached routine
    #         cached_stack = cache.get_records(query=form, count=howmany)
    #         entities = db_records_to_entity(register=entity_register, stack=cached_stack)
    #         companies = ResponseRoot(pocetCelkem=len(entities), ekonomickeSubjekty=entities)
    #
    #     else:
    #         # get data from site
    #         companies = serch_ares(search)
    #         if not companies:
    #             create_message_box(message=f"No response from ARES", title='CloakNDagger MessageBox',
    #                                description='')
    #
    #         else:
    #             if len(companies.ekonomickeSubjekty) > howmany:
    #                 cache.save_to_cache(query=form, entities=companies.ekonomickeSubjekty[howmany:])
    #                 companies = ResponseRoot(pocetCelkem=len(companies.ekonomickeSubjekty),
    #                                          ekonomickeSubjekty=companies.ekonomickeSubjekty[:howmany])
    #
    #     # for company in companies.ekonomickeSubjekty:
    #     #     entity_from_model(model=company, response=response)
    #     #
    #     # in_cache = cache.query_cache_size(query=form)
    #     # create_message_box(message=f"In cache left f'{in_cache}'", title='CloakNDagger MessageBox', description='')

# transform input to form attributes
    form = RequestFormEkonomickySubjekt(**input_company.model_dump())

    # invoke formular
    ares_logger.debug('Invoke  modal form')
    form = create_dynamic_form(model_class=RequestFormEkonomickySubjekt,
                               init_values=form.model_dump(),
                               title='Ares search',
                               description='Fill the form to search in ARES',
                               default_fields=[name for name in
                                               form.model_dump(exclude_none=True, exclude_unset=True,
                                                               exclude_defaults=True).keys()])

    # transform form to request format
    search = RequestEkonomickySubjekt(**form.model_dump())

    cache = TiDBCache(db_path=config.db.db_path)
    # cache using form as query because of user input

    if cache.query_cache_size(query=form) > 0:
        # cached routine
        cached_stack = cache.get_records(query=form, count=howmany)
        entities = db_records_to_entity(register=entity_register, stack=cached_stack)
        companies = ResponseRoot(pocetCelkem=len(entities), ekonomickeSubjekty=entities)

    else:
        # get data from site
        companies = serch_ares(search)

        if len(companies.ekonomickeSubjekty) > howmany:
            cache.save_to_cache(query=form, entities=companies.ekonomickeSubjekty[howmany:])
            companies = ResponseRoot(pocetCelkem=len(companies.ekonomickeSubjekty),
                                     ekonomickeSubjekty=companies.ekonomickeSubjekty[:howmany])

    if not companies:
        create_message_box(message=f"No response from ARES", title='CloakNDagger MessageBox',
                           description='')
    else:
        for company in companies.ekonomickeSubjekty:
            entity_from_model(model=company, response=response)

        in_cache = cache.query_cache_size(query=form)
        create_message_box(message=f"In cache left f'{in_cache}'", title='CloakNDagger MessageBox', description='')


