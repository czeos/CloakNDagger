from typing import List
from pydantic import BaseModel, model_validator, Field

from config import BASE_PATH
from tools.entities import SocialMediaProfile
from tools.base import EntitySetting, BaseEntityStack, EntityIcon
from tools.icons import WEB_PROFILE
from tools.utils import load_json, convert_image_to_base64, extract_domain


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


class UserProfile(SocialMediaProfile):
    site: str
    domain: str
    # #
    @model_validator(mode='before')
    @classmethod
    def set_fields(cls, data: dict) -> dict:
        url = data.get('url')

        #set domain
        _, domain, suffix = extract_domain(url)
        data['domain'] = f"{domain}.{suffix}"

        logo_path = LOGOS.get(f"{domain}_{suffix}")

        #set icon
        if logo_path:
            data['icon'] = EntityIcon(url=convert_image_to_base64(logo_path))
        else:
            data['icon'] = EntityIcon(url=WEB_PROFILE)
        return data


class UserProfiles(BaseEntityStack):
    results: int
    data: List[UserProfile]









