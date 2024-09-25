from typing import Type
from maltego_trx.overlays import OverlayPosition, OverlayType

from pydantic import ConfigDict, Field, AnyUrl, model_validator, field_validator
from tools.base import BaseEntity, EntitySetting, RegisterMeta, EntityIcon, EntityNote, EntityDisplay, EntityDisplayInfo
from tools.icons import EMAIL, IP, WEB_PROFILE, WEBPAGE, COMMENT, IMAGE, TARGET, TAG, IDENTIFICATOR, TAVILY,  ADRESS



#todo: change loction of hunchly case
#todo: refctor regiter
#todo: add base entiies: person, address, ico
#todo: create ico as matego entity in appliction and crete configurtion, add iconto tools/icon
#todo: refactor as module


class Case(BaseEntity):
    setting: EntitySetting = Field(default=EntitySetting(type='cnd.HunchlyCase',
                                                         main_attribute='name',
                                                         match='strict'))
    id: int = Field(default=0)
    name: str = Field(default='')


class Page(BaseEntity, extra='allow'):
    setting: EntitySetting = Field(default=EntitySetting(type='cnd.Webpage',
                                                         main_attribute='title',
                                                         match='strict'))
    url: AnyUrl
    title: str
    icon: EntityIcon = EntityIcon(url=WEBPAGE)


class Email(BaseEntity):
    setting: EntitySetting = Field(default=EntitySetting(type='cnd.Email',
                                                         main_attribute='email',
                                                         match='strict'))
    icon: EntityIcon = EntityIcon(url=EMAIL)
    email: str


class IPV4(BaseEntity):
    setting: EntitySetting = Field(default=EntitySetting(type='cnd.IPV4',
                                                         main_attribute='ipv4',
                                                         match='strict'))
    icon: EntityIcon = EntityIcon(url=IP)
    ipv4: str = Field(validation_alias='data_record')


class IPV6(BaseEntity):
    setting: EntitySetting = Field(default=EntitySetting(type='cnd.IPV6',
                                                         main_attribute='ipv6',
                                                         match='strict'))
    icon: EntityIcon = EntityIcon(url=IP)
    ipv6: str


class GoogleAnalytics(BaseEntity):
    setting: EntitySetting = Field(default=EntitySetting(type='cnd.GoogleAnalytics',
                                                         main_attribute='id',
                                                         match='strict'))
    id: str
    icon: EntityIcon = EntityIcon(url=IDENTIFICATOR)


class FacebookPixel(BaseEntity):
    setting: EntitySetting = Field(default=EntitySetting(type='cnd.FacebookPixel',
                                                         main_attribute='id',
                                                         match='strict'))
    id: str
    icon: EntityIcon = EntityIcon(url=IDENTIFICATOR)


class TorService(BaseEntity):
    setting: EntitySetting = Field(default=EntitySetting(type='cnd.TorService',
                                                         main_attribute='url',
                                                         match='strict'))
    url: str


class SocialMediaProfile(BaseEntity):
    setting: EntitySetting = Field(default=EntitySetting(type='cnd.SocialMediaAccount',
                                                         main_attribute='url',
                                                         match='strict'))

    url: str
    icon: EntityIcon = Field(default=EntityIcon(url=WEB_PROFILE))


class Photo(BaseEntity):
    """
    url     - location on net
    path    - location on file system
    """
    setting: EntitySetting = Field(default=EntitySetting(type='cnd.Photo',
                                                         main_attribute='name',
                                                         match='strict'))
    hash: str = Field(default='')
    url: str = Field(default='')
    path: str = Field(default='')
    name: str = Field(default='')
    icon: EntityIcon = EntityIcon(url=IMAGE)

    @field_validator('url')
    @classmethod
    def set_icon(cls, url):
        return EntityIcon(url=url)


class Selector(BaseEntity):
    setting: EntitySetting = Field(default=EntitySetting(type='cnd.Selector',
                                                         main_attribute='name',
                                                         match='strict'))
    name: str
    icon: EntityIcon = EntityIcon(url=TARGET)
    uuid: None = Field(default=None, description='Selector is unique accross the all cases')


class Tag(BaseEntity):
    setting: EntitySetting = Field(default=EntitySetting(type='cnd.Tag',
                                                         main_attribute='name',
                                                         match='strict'))
    name: str
    icon: EntityIcon = EntityIcon(url=TAG)
    uuid: None = Field(default=None, description='Selector is unique accross the all cases')


class Username(BaseEntity):
    setting: EntitySetting = Field(default=EntitySetting(type='cnd.Username',
                                                         main_attribute='username',
                                                         match='strict'))
    username: str


class Alias(BaseEntity):
    setting: EntitySetting = Field(default=EntitySetting(type='cnd.Alias',
                                                         main_attribute='alias',
                                                         match='strict'))
    alias: str = Field(default='')


class CloakNDagger(BaseEntity):
    setting: EntitySetting = Field(default=EntitySetting(type='cnd.CloakNDagger',
                                                         main_attribute='moto',
                                                         match='strict'))
    moto: str


class Text(BaseEntity):
    setting: EntitySetting = Field(default=EntitySetting(type='cnd.Text',
                                                         main_attribute='text',
                                                         match='strict'))
    text: str = Field(default='')
    icon: EntityIcon = EntityIcon(url=COMMENT)

    @model_validator(mode='before')
    @classmethod
    def set_note(cls, data):
        data['note'] = EntityNote(note=data['text'])
        return data


class Company(BaseEntity):
    setting: EntitySetting = Field(default=EntitySetting(type='maltego.Company',
                                                         main_attribute='name',
                                                         match='strict'))
    name: str = Field(default='')


class Person(BaseEntity):
    setting: EntitySetting = Field(default=EntitySetting(type='maltego.Person',
                                                         main_attribute='fullname',
                                                         match='strict'))
    fullname: str = Field(default='')


class Tavily(BaseEntity):
    setting: EntitySetting = EntitySetting(type='cnd.Tavily', match='strict', main_attribute='query')
    query: str = Field(default='Ask me', alias='query')
    icon: EntityIcon = EntityIcon(url=TAVILY)


class TestEntity(BaseEntity):
    setting: EntitySetting = Field(default=EntitySetting(type='cnd.test_entity',
                                                         main_attribute='fullname',
                                                         match='strict'))
    fullname: str = Field(default='')
    icon: EntityIcon = EntityIcon(url=TARGET)
    note: EntityNote = EntityNote(note='Test entity note')
    display_info: EntityDisplayInfo = EntityDisplayInfo(content='Test entity content', title='Test entity title:')
    overlay_text: EntityDisplay = EntityDisplay(value='Test entity overlay', position=OverlayPosition.SOUTH_WEST, overlay_type=OverlayType.TEXT)
    overlay_color: EntityDisplay = EntityDisplay(value='#45e06f', position=OverlayPosition.WEST, overlay_type=OverlayType.COLOUR)
    overlay_icon: EntityDisplay = EntityDisplay(value=TAG, position=OverlayPosition.NORTH, overlay_type=OverlayType.IMAGE)

class Adress(BaseEntity):
    setting: EntitySetting = Field(default=EntitySetting(type='cnd.adress_entity',
                                                         main_attribute='sidlo',
                                                         match='strict'))
    sidlo: str = Field(default='')
    icon: EntityIcon = Field(default=EntityIcon(url=ADRESS))


# Define the Register class using the dynamic metaclass
class Register(metaclass=RegisterMeta):
    """
    All entities are registered here
    Entities are registered dynamically and wrapped in EntityWrapper
    attributes:
        clas: class of entity
        name: type of entity i.e. return value of entity.setting.type
    """
    CASE: Type[BaseEntity] = Case
    PAGE: Type[BaseEntity] = Page
    EMAIL: Type[BaseEntity] = Email
    IPV4: Type[BaseEntity] = IPV4
    IPV6: Type[BaseEntity] = IPV6
    GOOGLE_ANALYTICS: Type[BaseEntity] = GoogleAnalytics
    FACEBOOK_PIXEL: Type[BaseEntity] = FacebookPixel
    TOR_SERVICE: Type[BaseEntity] = TorService
    SOCIAL_MEDIA_ACCOUNT: Type[BaseEntity] = SocialMediaProfile
    PHOTO: Type[BaseEntity] = Photo
    SELECTOR: Type[BaseEntity] = Selector
    TAG: Type[BaseEntity] = Tag
    USERNAME: Type[BaseEntity] = Username
    ALIAS: Type[BaseEntity] = Alias
    CLOAK_N_DAGGER: Type[BaseEntity] = CloakNDagger
    TEXT: Type[BaseEntity] = Text
    COMPANY: Type[BaseEntity] = Company
    PERSON: Type[BaseEntity] = Person
    TAVILY: Type[BaseEntity] = Tavily
    TEST_ENTITY: Type[BaseEntity] = TestEntity
    ADRESS: Type[BaseEntity] = Adress

ENTITYREG = Register()
