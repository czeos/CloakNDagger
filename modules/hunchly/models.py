from typing import List, Any, Optional
from pydantic import BaseModel, AnyUrl, Field, model_validator, field_validator
from datetime import datetime
from pathlib import Path

from base import BaseEntity

class Tag(BaseModel):
    id: int
    case_id: int
    tag_name: str


class Page(BaseEntity):
    id: int
    case_id: int
    created: datetime = Field(validation_alias='timestamp_created')
    updated: datetime = Field(validation_alias='timestamp_updated')
    url: AnyUrl
    title: str
    hash: str = Field(validation_alias='content_hash')
    # is_important: bool
    # synced_at: datetime
    # tags: List[Tag]
    _entity_type: str = 'cnd.HunchlyWebpage'
    _entity_attr: str = 'title'
    _entity_match_type: str = 'strict'


class Pages(BaseModel):
    number_of_results: int
    pages: List[Page]


class PageData(BaseEntity):
    type: str = Field(validation_alias='data_type')
    extractor: str = Field(validation_alias='data_extractor')
    record: str = Field(validation_alias='data_record')
    _entity_type: str = 'cnd.HunchlyPageData'
    _entity_attr: str = 'record'
    _entity_match_type: str = 'strict'


class PageDatas(BaseModel):
    number_of_results: int
    data: List[PageData]


class Photo(BaseEntity):
    hash: str = Field(validation_alias='photo_hash')
    url: str = Field(validation_alias='photo_url')
    path: str = Field(validation_alias='photo_local_file_path')
    exif_data: bool = Field(validation_alias='exif_data')
    name: str
    _entity_type: str = 'maltego.Image'
    _entity_attr: str = 'name'
    _entity_match_type: str = 'strict'

    @model_validator(mode='before')
    @classmethod
    def set_fields(cls, data: dict) -> dict:
        if not data.get('exif_data'):
            data['exif_data'] = False
        else:
           data['exif_data'] = True

        if data['photo_url']:
            data['name'] = Path(data['photo_url']).name
        return data


class Photos(BaseModel):
    number_of_results: int
    photos: List[Photo]


class Selector(BaseEntity):
    id: int = Field(validation_alias='selector_id')
    name: str = Field(validation_alias='selector')
    _entity_type: str = 'cnd.HunchlySelector'
    _entity_attr: str = 'name'
    _entity_match_type: str = 'strict'


class Selectors(BaseModel):
    number_of_results: int
    data: List[Selector] = Field(validation_alias='selectors')


class Tag(BaseEntity):
    id: int = Field(validation_alias='id')
    name: str = Field(validation_alias='tag_name')
    _entity_type: str = 'cnd.HunchlyTag'
    _entity_attr: str = 'name'
    _entity_match_type: str = 'strict'


class Tags(BaseModel):
    number_of_results: int
    data: Optional[List[Tag]] = Field(validation_alias='tags')

    @field_validator('data')
    @classmethod
    def set_list(cls, value: List) -> List:
        if not isinstance(value, list):
            return []
        return value