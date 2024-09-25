import pytest

from modules.whatsmynameapp.api import check_site, check_all_sites, get_site_dat, HEADERS
from modules.whatsmynameapp.models import Site, UserProfile, WhatsMyNameData


from unittest.mock import patch, MagicMock
from maltego_trx.maltego import MaltegoTransform, MaltegoMsg
from transforms.Whatmynameapp_AliasToWebProfile import Whatmynameapp_AliasToWebProfile
from tools.entities import Alias

site = Site(name="example", uri_check="http://example.com/{account}", e_string="exists", m_string="missing",
            e_code=200, m_code=404,known=["username"], cat="social")
site1 = Site(name="example1", uri_check="http://example1.com/{account}", e_string="exists", m_string="missing",
             e_code=200, m_code=404,known=["username"], cat="social")
site2 = Site(name="example2", uri_check="http://example2.com/{account}", e_string="exists", m_string="missing",
             e_code=200, m_code=404,known=["username"], cat="social")

@patch('modules.whatsmynameapp.api.requests.get')
def test_check_site_returns_user_profile_when_site_matches(mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.text = "exists"
    result = check_site(site, "username", HEADERS)
    assert isinstance(result, UserProfile)
    assert result.site == "example"

@patch('modules.whatsmynameapp.api.requests.get')
def test_check_site_returns_none_when_site_does_not_match(mock_get):
    mock_get.return_value.status_code = 404
    mock_get.return_value.text = "missing"
    result = check_site(site, "username", HEADERS)
    assert result is None

@patch('modules.whatsmynameapp.api.requests.get')
def test_check_site_handles_exceptions_gracefully(mock_get):
    mock_get.side_effect = Exception("Network error")
    result = check_site(site, "username", HEADERS)
    assert result is None

@patch('modules.whatsmynameapp.api.requests.get')
def test_check_all_sites_returns_list_of_user_profiles(mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.text = "exists"
    result = check_all_sites([site1, site2], "username", HEADERS)
    assert len(result) == 2
    assert isinstance(result[0], UserProfile)
    assert isinstance(result[1], UserProfile)

@patch('modules.whatsmynameapp.api.requests.get')
def test_check_all_sites_returns_empty_list_when_no_sites_match(mock_get):
    mock_get.return_value.status_code = 404
    mock_get.return_value.text = "missing"
    result = check_all_sites([site1, site2], "username", HEADERS)
    assert result == []

@patch('modules.whatsmynameapp.api.requests.get')
def test_get_site_dat_returns_whatsmyname_data(mock_get):
    mock_get.return_value.json.return_value = {
        "sites": [site.model_dump()],
        "categories": ["social"],
    }
    result = get_site_dat("http://example.com/data.json")
    assert isinstance(result, WhatsMyNameData)
    assert result.sites[0].name == "example"



@patch('transforms.Whatmynameapp_AliasToWebProfile.TiDBCache')
@patch('transforms.Whatmynameapp_AliasToWebProfile.model_from_maltego_request')
@patch('transforms.Whatmynameapp_AliasToWebProfile.create_entity_from_model')
def test_Search_profiles_by_username_with_cache(mock_create_entity, mock_model_from_request, mock_cache):
    request = MagicMock(spec=MaltegoMsg)
    response = MagicMock(spec=MaltegoTransform)
    mock_model_from_request.return_value = Alias(alias='testuser')
    mock_cache.return_value.exist_table.return_value = True
    mock_cache.return_value.get_records.return_value = ['record1', 'record2']
    mock_cache.return_value.query_cache_size.return_value = 2

    Whatmynameapp_AliasToWebProfile.create_entities(request, response)

    mock_cache.return_value.exist_table.assert_called_once_with(query='testuser')
    mock_cache.return_value.get_records.assert_called_once_with(query='testuser', count=12)
    mock_create_entity.assert_called()
