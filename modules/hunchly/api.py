import json
from functools import partial
from subprocess import Popen, PIPE
from typing import List, Type, Union, Optional

from config import config
from modules.hunchly.models import HunchlyPageDatas, HunchlyPages, HunchlyPhotos, HunchlySelectors, HunchlyTags, HunchlyCases
from pydantic import BaseModel


def call_api(params: List[str], model: Type[BaseModel]) -> BaseModel:
    process = Popen(params, stdout=PIPE, stderr=PIPE)
    stdout, stderr = process.communicate()
    result = json.loads(stdout)
    return model(**result)


def set_api(params: List[str], model: Type[BaseModel], var: Optional[Union[int, str]] = None) -> BaseModel:
    if not var:
        return call_api(params=params, model=model)
    return call_api(params=params + [var], model=model)

get_cases = partial(set_api, [config.hunchly.api_path, "case", "get"], HunchlyCases)
get_case_pages = partial(set_api, [config.hunchly.api_path, "page", "list", "-n"], HunchlyPages)
get_case_data = partial(set_api, [config.hunchly.api_path, "caseData", "-n"], HunchlyPageDatas)
get_page_data = partial(set_api, [config.hunchly.api_path, "caseData", "-p"], HunchlyPageDatas)
get_page_photo = partial(set_api, [config.hunchly.api_path, "photo", "get", "-p"], HunchlyPhotos)
get_case_photo = partial(set_api, [config.hunchly.api_path, "photo", "get", "-n"], HunchlyPhotos)
get_page_selectors = partial(set_api, [config.hunchly.api_path, "selector", "get", "-p"], HunchlySelectors)
get_case_selectors = partial(set_api, [config.hunchly.api_path, "selector", "get", "-n"], HunchlySelectors)
get_page_tags = partial(set_api, [config.hunchly.api_path, "tag", "get", "-p"], HunchlyTags)
get_case_tags = partial(set_api, [config.hunchly.api_path, "tag", "get", "-n"], HunchlyTags)


if __name__ == '__main__':
    # c = get_cases(' ')
    # c = get_case_pages(' ')
    # a = get_case_data("RusPhone 12")
    # get_page_data('429')
    # aa = get_case_photo('sshr')
    # a = get_page_photo('446')
    # aa = get_case_selectors('sshr')
    # a = get_page_selectors('429')
    # aa = get_case_tags('sshr')
    # a = get_page_tags('453')
    # a = get_page_tags('446')
    a = get_cases()
    pass