from maltego_trx.transform import DiscoverableTransform
from maltego_trx.maltego import MaltegoTransform, MaltegoMsg

from extensions import registry
from settings import whatsmynameapp_transformset
from modules.whatsmynameapp.api import get_site_dat, check_all_sites, HEADERS
from modules.whatsmynameapp.models import UserProfiles
from config import config
from tools.gui.components import message_box
from tools.maltego import create_entity_from_model, model_from_maltego_request
from tools.dbs import TiDBCache, db_records_to_entity
from tools.entities import  Alias, ENTITYREG
from tools.base import BaseEntityStack


@registry.register_transform(
    display_name="Search profiles by username [WhatsMyNameApp]",
    input_entity=ENTITYREG.ALIAS.get_type(),
    description="Search web profiles by username",
    output_entities=['cnd.UserProfile'],
    transform_set=whatsmynameapp_transformset

)
class Whatmynameapp_AliasToWebProfile(DiscoverableTransform):
    """
    Get a page dat from Hunchly Case
    """
    @classmethod
    def create_entities(cls, request: MaltegoMsg, response: MaltegoTransform):
        # how many
        howmany = request.Slider
        howmany = 12

        # build query
        username = model_from_maltego_request(request=request, model=Alias)

        #cache
        cache = TiDBCache(db_path=config.db.db_path)

        if cache.exist_table(query=username):
            response.addUIMessage(f' exist cache routine')

            cached_stack = cache.get_records(query=username, count=howmany)
            entities = db_records_to_entity(register=ENTITYREG, stack=cached_stack)
            items = UserProfiles(results=cache.query_cache_size(username), data=entities)
        else:
            response.addUIMessage(f' request routine')

            wmnd = get_site_dat(config.whatsmynmeapp.data)
            profiles = check_all_sites(wmnd.sites, username.alias, HEADERS)
            items = UserProfiles(results=len(profiles), data=profiles)
            cache.save_to_cache(query=username, stack=items)

        # generating of pages
        for item in items.data:
            create_entity_from_model(item, response)

        message_box(message=f"On WhatsMyNameApp were found profiles for username {username.alias}. "
                              f"In cache {items.results} left", title='CloakNDagger MessageBox', description='')
        response.addUIMessage(f"On WhatsMyNameApp were found profiles for username {username.alias}. "
                              f"In cache {items.results} left")
