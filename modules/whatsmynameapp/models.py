from typing import List, Type, Union
from pydantic import BaseModel, model_validator, Field
from requests import get

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


        try:
            logo_path = LOGOS.get(f"{domain}_{suffix}")
            icon = EntityIcon(url=convert_image_to_base64(logo_path))
        except FileNotFoundError:
            url = f"https://logo.clearbit.com/{domain}.{suffix}"
            response = get(f"https://logo.clearbit.com/{domain}.{suffix}")
            if response.status_code == 200:
                icon = EntityIcon(url=url)
            else:
                icon = EntityIcon(url=WEB_PROFILE)


        data['icon'] = icon
        return data


class UserProfiles(BaseEntityStack):
    results: int
    data: List[Union[SocialMediaProfile, UserProfile]]









