from typing import List
from pydantic import BaseModel
import requests

from modules.tavily.models import  Response, TavilyPage, TavilyPhoto, SearchRequest
from tools.base import BaseEntity
from tools.entities import Text


def tivaly_api(request: SearchRequest) -> Response:
    url = "https://api.tavily.com/search"
    response = requests.post(url, json=request.model_dump())
    if response.status_code == 200:
        return Response(**response.json())


def response_to_entities(response: Response) -> List[BaseEntity]:
    entities = []
    if response.answer:
        entities += [Text(text=response.answer)]
    if response.images:
        entities += [TavilyPhoto(url=img) for img in response.images]
    if response.results:
        entities += [TavilyPage(**page.model_dump()) for page in response.results]
    return entities
