import requests
from modules.rejstrik.models import Root


def find_relations(ico: str) -> Root:
    url = f"https://rejstrik-firem.kurzy.cz/services/graph/CZC{ico}"
    h = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:130.0) Gecko/20100101 Firefox/130.0",
        "Host": "rejstrik-firem.kurzy.cz",
        "Accept-enconding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Accept": "*/*",
    }
    s = requests.Session()
    s.headers.update(h)
    response = s.get(url,headers=h,allow_redirects=True)
    j = response.json()
    if response.status_code == 200:
        return Root(**j)