import concurrent.futures
from typing import List, Dict, Optional
import requests

from modules.whatsmynameapp.models import Site, WhatsMyNameData, UserProfile



HEADERS = {
    "Accept": "text/html, application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "accept-language": "en-US;q=0.9,en,q=0,8",
    "accept-encoding": "gzip, deflate",
    "user-Agent": "Mozilla/5.0 (Windows NT 10.0;Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36",
}


def check_site(site: Site, username: str, headers: dict) -> Optional[UserProfile]:
    site_name = site.name
    uri_check = site.uri_check.format(account=username)
    try:
        res = requests.get(uri_check, headers=headers, timeout=10)
        estring_pos = site.e_string in res.text
        estring_neg = site.m_string in res.text

        if res.status_code == site.e_code and estring_pos and not estring_neg:
            return UserProfile(site=site_name, uri=uri_check)
    except Exception as e:
        pass


def check_all_sites(sites: List[Site], username: str, headers: dict) -> List[UserProfile]:
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        futures = [executor.submit(check_site, site, username, headers) for site in sites]
        results = [future.result() for future in concurrent.futures.as_completed(futures) if future.result() is not None]
    return results


def get_site_dat(url: str) -> WhatsMyNameData:
    response = requests.get(url)
    data = response.json()
    return WhatsMyNameData(**data)


