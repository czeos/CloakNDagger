import json
from subprocess import Popen, PIPE
from config import HUNCHLY_API_PATH
from modules.hunchly.models import PageDatas, Pages, Photos, Selectors, Tags


def get_case_pages(case: str) -> Pages:

    process = Popen([HUNCHLY_API_PATH, "page", "list", "-n", case], stdout=PIPE, stderr=PIPE)
    stdout, stderr = process.communicate()

    try:
        result = json.loads(stdout)
        return Pages(**result)

    except Exception:
        raise Exception(f"Failed to retrieve results for Hunchly case: {case}")


def get_case_data(case: str) -> PageDatas:
    process = Popen([HUNCHLY_API_PATH, "caseData", "-n", case], stdout=PIPE, stderr=PIPE)
    stdout, stderr = process.communicate()
    try:
        result = json.loads(stdout)
        return PageDatas(**result)

    except Exception:
        raise Exception(f"Failed to retrieve results for Case: {case}")


def get_page_data(page_id: int) -> PageDatas:
    process = Popen([HUNCHLY_API_PATH, "caseData", "-p", page_id], stdout=PIPE, stderr=PIPE)
    stdout, stderr = process.communicate()
    try:
        result = json.loads(stdout)
        return PageDatas(**result)

    except Exception:
        raise Exception(f"Failed to retrieve results for Page ID: {page_id}")


def get_page_photo(page_id: int) -> Photos:
    process = Popen([HUNCHLY_API_PATH, 'photo', 'get', '-p', page_id], stdout=PIPE, stderr=PIPE)
    stdout, stderr = process.communicate()
    try:
        result = json.loads(stdout)
        return Photos(**result)

    except Exception:
        raise Exception(f"Failed to retrieve results for Page ID: {page_id}")

def get_case_photo(case: str) -> Photos:
    process = Popen([HUNCHLY_API_PATH, 'photo', 'get', '-n', case], stdout=PIPE, stderr=PIPE)
    stdout, stderr = process.communicate()
    try:
        result = json.loads(stdout)
        return Photos(**result)

    except Exception:
        raise Exception(f"Failed to retrieve results for Case: {case}")


def get_page_selectors(page_id: int) -> Selectors:
    process = Popen([HUNCHLY_API_PATH, 'selector', 'get', '-p', page_id], stdout=PIPE, stderr=PIPE)
    stdout, stderr = process.communicate()
    try:
        result = json.loads(stdout)
        return Selectors(**result)

    except Exception:
        raise Exception(f"Failed to retrieve results for Page ID: {page_id}")


def get_case_selectors(case: str) -> Selectors:
    process = Popen([HUNCHLY_API_PATH, 'selector', 'get', '-n', case], stdout=PIPE, stderr=PIPE)
    stdout, stderr = process.communicate()
    try:
        result = json.loads(stdout)
        return Selectors(**result)

    except Exception:
        raise Exception(f"Failed to retrieve results for Case: {case}")


def get_page_tags(page_id: int) -> Tags:
    process = Popen([HUNCHLY_API_PATH, 'tag', 'get', '-p', page_id], stdout=PIPE, stderr=PIPE)
    stdout, stderr = process.communicate()
    try:
        result = json.loads(stdout)
        return Tags(**result)

    except Exception:
        raise Exception(f"Failed to retrieve results for Page ID: {page_id}")


def get_case_tags(case: str) -> Tags:
    process = Popen([HUNCHLY_API_PATH, 'tag', 'get', '-n', case], stdout=PIPE, stderr=PIPE)
    stdout, stderr = process.communicate()
    try:
        result = json.loads(stdout)
        return Tags(**result)

    except Exception:
        raise Exception(f"Failed to retrieve results for Case: {case}")




if __name__ == '__main__':
    # c = get_case_pages('sshr')
    # get_case_data('sshr')
    # get_page_data('429')
    # aa = get_case_photo('sshr')
    # a = get_page_photo('429')
    # aa = get_case_selectors('sshr')
    # a = get_page_selectors('429')
    # aa = get_case_tags('sshr')
    a = get_page_tags('453')
    a = get_page_tags('446')
    pass