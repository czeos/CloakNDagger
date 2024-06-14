from datetime import datetime
from pathlib import Path
from typing import List, Optional, Union, Literal

from pydantic import AnyUrl, Field, model_validator, field_validator, AliasChoices

from tools.base import BaseEntityStack
from tools.entities import (Case, Page, Email, IPV4, IPV6, GoogleAnalytics,
                            FacebookPixel, TorService, SocialMediaProfile, Photo, Selector, Tag)
from tools.icons import VKONTAKTE
from tools.utils import convert_image_to_base64


class HunchlyCase(Case):
    id: int = Field(validation_alias=AliasChoices('id', 'case_id'))
    name: str = Field(validation_alias=AliasChoices('name', 'case_name'))


class HunchlyCases(BaseEntityStack):
    results: int = Field(validation_alias='number_of_results')
    data: List[HunchlyCase] = Field(validation_alias='cases', default_factory=list)


class HunchlyPage(Page):
    id: int
    case_id: int
    created: datetime = Field(validation_alias='timestamp_created')
    updated: datetime = Field(validation_alias='timestamp_updated')
    url: AnyUrl
    title: str
    hash: str = Field(validation_alias='content_hash')


class HunchlyPages(BaseEntityStack):
    results: int = Field(validation_alias='number_of_results')
    data: List[HunchlyPage] = Field(validation_alias='pages', default_factory=list)


class HunchlyEmail(Email):
    type: str = Field(validation_alias='data_type')
    extractor: Literal['Email Address'] = Field(validation_alias='data_extractor')
    email: str = Field(validation_alias='data_record')


class HunchlyIPV4(IPV4):
    type: str = Field(validation_alias='data_type')
    extractor: Literal['IPv4 IP Address'] = Field(validation_alias='data_extractor')
    ipv4: str = Field(validation_alias='data_record')


class HunchlyIPV6(IPV6):
    type: str = Field(validation_alias='data_type')
    extractor: Literal['IPv6 IP Address'] = Field(validation_alias='data_extractor')
    ipv6: str = Field(validation_alias='data_record')


class HunchlyGoogleAnalytics(GoogleAnalytics):
    type: str = Field(validation_alias='data_type')
    extractor: Literal['Google Analytics'] = Field(validation_alias='data_extractor')
    id: str = Field(validation_alias='data_record')


class HunchlyFacebookPixel(FacebookPixel):
    type: str = Field(validation_alias='data_type',)
    extractor: Literal['Facebook Tracking Pixel ID'] = Field(validation_alias='data_extractor')
    id: str = Field(validation_alias='data_record')


class HunchlyTorService(TorService):
    type: str = Field(validation_alias='data_type')
    extractor: Literal['Tor Hidden Service'] = Field(validation_alias='data_extractor')
    url: str = Field(validation_alias='data_record')


class HunchlyVKontakteProfile(SocialMediaProfile):
    type: str = Field(validation_alias='data_type')
    extractor: Literal['VKontakte User'] = Field(validation_alias='data_extractor')
    url: str = Field(validation_alias='data_record')
    icon: str = VKONTAKTE


HUNCHLY_DATA_TYPES = {'Email Address': HunchlyEmail,
                    'IPv4 IP Address': HunchlyIPV4,
                    'IPv6 IP Address': HunchlyIPV6,
                    'Google Analytics': HunchlyGoogleAnalytics,
                    'Facebook Tracking Pixel ID': HunchlyFacebookPixel,
                    'Tor Hidden Service': HunchlyTorService,
                    'VKontakte User': HunchlyVKontakteProfile}

#set o types
HUNCHLY_DATA_TYPES_LITERALS = Union[tuple(HUNCHLY_DATA_TYPES.values())]


class HunchlyPageDatas(BaseEntityStack):
    results: int = Field(validation_alias='number_of_results')
    data: List[HUNCHLY_DATA_TYPES_LITERALS] = Field(default_factory=list)


class HunchlyPhoto(Photo):
    hash: str = Field(validation_alias='photo_hash')
    url: str = Field(validation_alias='photo_url')
    path: str = Field(validation_alias='photo_local_file_path')
    exif_data: bool = Field(validation_alias='exif_data')
    name: str
    icon: str = Field(default='')


    @model_validator(mode='before')
    @classmethod
    def set_fields(cls, data: dict) -> dict:
        if not data.get('exif_data'):
            data['exif_data'] = False
        else:
           data['exif_data'] = True

        if data['photo_url']:
            data['name'] = Path(data['photo_url']).name

        data['icon'] = convert_image_to_base64(data['photo_local_file_path'])
        return data


class HunchlyPhotos(BaseEntityStack):
    results: int = Field(validation_alias='number_of_results')
    data: List[HunchlyPhoto] = Field(validation_alias='photos', default_factory=list)


class HunchlySelector(Selector):
    id: int = Field(validation_alias='selector_id')
    name: str = Field(validation_alias='selector')


class HunchlySelectors(BaseEntityStack):
    results: int = Field(validation_alias='number_of_results')
    data: List[HunchlySelector] = Field(validation_alias='selectors', default_factory=list)



class HunchlyTag(Tag):
    id: int = Field(validation_alias='id')
    name: str = Field(validation_alias='tag_name')


class HunchlyTags(BaseEntityStack):
    results: int = Field(validation_alias='number_of_results')
    data: Optional[List[HunchlyTag]] = Field(validation_alias='tags', default_factory=list)

    @field_validator('data')
    @classmethod
    def set_list(cls, value: List) -> List:
        if not isinstance(value, list):
            return []
        return value