from typing import List
from pydantic import BaseModel
import requests

from modules.tavily.models import Tavily, Response, TavilyPage, TavilyPhoto
from tools.base import BaseEntity
from tools.entities import Text

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

def tivaly_api(request: Tavily):
    params = SearchRequest(**request.dict())
    url = "https://api.tavily.com/search"
    response = requests.post(url, json=params.dict())
    if response.status_code == 200:
        return Response(**response.json())


def response_to_entities(response: Response) -> List[BaseEntity]:
    entites = []
    if response.answer:
        entites += [Text(text=response.answer)]
    if response.images:
        entites += [TavilyPhoto(url=img) for img in response.images]
    if response.results:
        entites += [TavilyPage(**page.dict()) for page in response.results]
    return entites
