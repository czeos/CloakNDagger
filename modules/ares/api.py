from modules.ares.models import Company
from modules.ares import ares_logger
from typing import Any, Dict
import requests
from modules.ares.models import RequestEkonomickySubjekt,Root

#TODO: add the real implementation
def serch_ares(payload: RequestEkonomickySubjekt):
    ares_logger.debug('logger test')
    root = make_request(payload)
    while root and root.pocetCelkem > payload.start:
        payload.start += 10
        root.ekonomickeSubjekty += make_request(payload).ekonomickeSubjekty

    return root

def make_request(payload: RequestEkonomickySubjekt) -> Root:
    response = requests.post("https://ares.gov.cz/ekonomicke-subjekty-v-be/rest/ekonomicke-subjekty/vyhledat",
                             json=payload.model_dump(exclude_none=True))
    if response.status_code == 200:
        return Root(**response.json())