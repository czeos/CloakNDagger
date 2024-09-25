from typing import List
from typing import Optional
from pydantic import BaseModel, Field, model_validator, AliasChoices
from tools.entities import Page, Photo
from tools.utils import extract_domain
from tools.base import EntityIcon


class SearchRequest(BaseModel):
    api_key: str
    query: str
    search_depth: str = "basic"
    include_answer: bool = False
    include_images: bool = True
    include_raw_content: bool = False
    max_results: int = 5
    include_domains: list = []
    exclude_domains: list = []


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
        data['icon'] = EntityIcon(url=data['url'])
        return data


class TavilyPage(Page):
    content: Optional[str] = Field(default='')
    published: Optional[str] = Field(default='')
    content: str = Field(default='')
    raw_content: Optional[str] = Field(default=None)
