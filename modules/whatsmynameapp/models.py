from typing import List

from pydantic import BaseModel, model_validator, Field

from config import BASE_PATH
from tools.base import BaseEntity, EntitySetting, BaseEntityStack
from tools.base import ENTITIES_TYPE_NAMES, entity_register
from tools.icons import WEB_PROFILE
from tools.utils import extract_domain
from tools.utils import load_json, convert_image_to_base64

ENTITIES_TYPE_NAMES.register(name='USER_PROFILE', item='cnd.UserProfile')
ENTITIES_TYPE_NAMES.register(name='LOGO', item='cnd.Logo')


LOGOS = load_json(BASE_PATH /'tools' / 'icons' / 'social_media' / 'logos.json')


class Site(BaseModel):
    name: str
    uri_check: str
    e_code: int
    e_string: str
    m_string: str
    m_code: int
    known: List[str]
    cat: str


class WhatsMyNameData(BaseModel):
    categories: List[str]
    sites: List[Site]


class Logo(BaseEntity):
    domain: str
    icon: str


class UserProfile(BaseEntity):
    setting: EntitySetting = Field(default=EntitySetting(type='cnd.UserProfile', main_attribute='site', match='strict'))
    site: str
    uri: str
    domain: str
    icon: str
    # #
    @model_validator(mode='before')
    @classmethod
    def set_fields(cls, data: dict) -> dict:
        uri = data.get('uri')

        #set domain
        _, domain, suffix = extract_domain(uri)
        data['domain'] = f"{domain}.{suffix}"

        logo_path = LOGOS.get(f"{domain}_{suffix}")

        #set icon
        if logo_path:
            data['icon'] = convert_image_to_base64(logo_path)
        else:
            data['icon'] = WEB_PROFILE
        return data



class UserProfiles(BaseEntityStack):
    results: int
    data: List[UserProfile]

entity_register.register(name=ENTITIES_TYPE_NAMES.USER_PROFILE, item=UserProfile)









