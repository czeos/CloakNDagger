from typing import List
from typing import Optional
from pydantic import BaseModel, Field, model_validator, AliasChoices
from tools.base import BaseEntity, EntitySetting, ENTITIES_TYPE_NAMES, entity_register
from config import config

from tools.icons import TAVILY
from tools.entities import Page, Photo
from tools.utils import extract_domain


class Tavily(BaseEntity):
    setting: EntitySetting = EntitySetting(type=ENTITIES_TYPE_NAMES.TAVILY, match='strict', main_attribute='query')
    api_key: str = Field(default=config.tavily.api_key)
    query: str = Field(default='Ask me', alias='query')
    search_depth: str = Field(default='basic', alias='search_depth')
    include_answer: bool = Field(default=False, alias='include_answer')
    include_images: bool = Field(default=False, alias='include_images')
    include_raw_content: bool = Field(default=False, alias='include_raw_content')
    max_results: int = Field(default=5, alias='max_results')
    include_domains: List[str] = Field(default_factory=list, alias='include_domains')
    exclude_domains: List[str] = Field(default_factory=list, alias='exclude_domains')
    icon: str = TAVILY


entity_register.register(name=ENTITIES_TYPE_NAMES.TAVILY, item=Tavily)


class Result(BaseModel):
    url: str = Field(default='')
    published: Optional[str] = Field(default=None, validation_alias=AliasChoices('published date'))
    title: str
    content: str = Field(default='')
    score: float
    raw_content: Optional[str] = Field(default='')


class Response(BaseModel):
    query: str = Field(default='')
    follow_up_questions: Optional[List[str]] = Field(default_factory=list)
    answer: Optional[str] = Field(default=None)
    images: Optional[List[str]] = Field(default_factory=None)
    results: List[Result] = Field(default_factory=None)
    response_time: float


class TavilyPhoto(Photo):

    @model_validator(mode='before')
    @classmethod
    def set_name(cls, data):
        subdomain, domain, suffix = extract_domain(data['url'])
        data['name'] = f'{subdomain}.{domain}.{suffix}'
        data['icon'] = data['url']
        return data


class TavilyPage(Page):
    content: Optional[str] = Field(default='')
    published: Optional[str] = Field(default='')
    content: str = Field(default='')
    raw_content: Optional[str] = Field(default=None)
