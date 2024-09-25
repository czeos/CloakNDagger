import pytest
from tools.base import BaseEntity, EntitySetting, EntityIcon, EntityNote, EntityDisplayInfo, MaltegoSettingAttributes

@pytest.fixture
def base_entity():
    return BaseEntity(
        setting=EntitySetting(type='cnd.Alias', main_attribute='alias', match='strict'),
        uuid='1234',
        icon=EntityIcon(url='http://example.com/icon.png'),
        display_info=EntityDisplayInfo(content='content', title='title'),
        note=EntityNote(note='This is a note')
    )

def test_initialization(base_entity):
    assert base_entity.setting.type == 'cnd.Alias'
    assert base_entity.uuid == '1234'
    assert base_entity.icon.url == 'http://example.com/icon.png'
    assert base_entity.display_info.content == 'content'
    assert base_entity.note.note == 'This is a note'

def test_entity_dump_default(base_entity):
    dumped = base_entity.entity_dump()
    assert 'setting' in dumped
    assert 'icon' in dumped
    assert 'display_info' in dumped
    assert 'note' in dumped
    assert 'uuid' in dumped
    assert dumped['uuid'] == '1234'

def test_entity_dump_exclude(base_entity):
    dumped = base_entity.entity_dump(exclude=['uuid'])
    assert 'uuid' not in dumped
    assert 'icon' in dumped
    assert dumped['icon'] == base_entity.icon.model_dump()

def test_entity_dump_exclude_maltego_setting_attributes(base_entity):
    dumped = base_entity.entity_dump(exclude=[MaltegoSettingAttributes])
    assert 'setting' not in dumped
    assert 'icon' not in dumped
    assert 'display_info' not in dumped
    assert 'note' not in dumped
    assert 'uuid' in dumped
    assert dumped['uuid'] == '1234'


def test_entity_dump_exclude_maltego_setting_attributes_subtype(base_entity):
    dumped = base_entity.entity_dump(exclude=[EntityIcon])
    assert 'setting' in dumped
    assert 'icon' not in dumped
    assert 'display_info' in dumped
    assert 'note' in dumped
    assert 'uuid' in dumped
    assert dumped['uuid'] == '1234'

def test_entity_dump_exclude_maltego_combination(base_entity):
    dumped = base_entity.entity_dump(exclude=[EntityIcon, 'uuid'])
    assert 'setting' in dumped
    assert 'icon' not in dumped
    assert 'display_info' in dumped
    assert 'note' in dumped
    assert 'uuid' not in dumped

def test_set_icon(base_entity):
    new_icon_url = 'http://example.com/new_icon.png'
    base_entity.set_icon(new_icon_url)
    assert base_entity.icon.url == new_icon_url

def test_set_note(base_entity):
    new_note = 'This is a new note'
    base_entity.set_note(new_note)
    assert base_entity.note.note == new_note

def test_set_display_info(base_entity):
    new_content = 'new content'
    new_title = 'new title'
    base_entity.set_display_info(new_content, new_title)
    assert base_entity.display_info.content == new_content
    assert base_entity.display_info.title == new_title


def test_hash(base_entity):
    new_content = 'new content'
    new_title = 'new title'
    base_entity.set_display_info(new_content, new_title)
    assert base_entity.display_info.content == new_content
    assert base_entity.display_info.title == new_title