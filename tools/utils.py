import hashlib
import json
from pathlib import Path
import base64
import envtoml
import httpx
import json

from tldextract import tldextract


def convert_image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


# Get website logo
def get_site_logo(domain_name):

    if domain_name == "t.me":
        logo = "https://logo.clearbit.com/telegram.org"
    elif domain_name == "giters.com":
        logo = "https://giters.com/images/favicon.svg"
    elif domain_name == "ko-fi.com":
        logo = "https://storage.ko-fi.com/cdn/brandasset/kofi_s_logo_nolabel.png"
    else:
        logo = f"https://logo.clearbit.com/{domain_name}"
    return logo


def test_url_success(url) -> bool:
    """Return true if status code 200 else false"""
    response = httpx.get(url)
    return response.is_success


def load_toml(path: Path) -> dict:
    """Read TOML file and return dict representation"""
    with open(path, 'r') as file:
        return envtoml.load(file)


def hash_fn(data: dict):
    json_string = json.dumps(data, sort_keys=True, ensure_ascii=False)
    hash_object = hashlib.sha256(json_string.encode('utf-8'))
    return str(hash_object.hexdigest())



def load_json(path):
    with open(path, 'r') as file:
        data = json.load(file)
        return data


def extract_domain(uri: str) -> tuple[str, str, str]:
    """

    :param uri: url
    :return: subomain, domain, suffix
    """
    tld = tldextract.extract(uri)
    return tld.subdomain, tld.domain, tld.suffix