from pydantic import Field, AnyUrl, model_validator
from tools.base import BaseEntity, EntitySetting
from tools.icons import EMAIL, IP, WEB_PROFILE, WEBPAGE, COMMENT, IMAGE, TARGET, TAG, IDENTIFICATOR
from tools.base import entity_register, ENTITIES_TYPE_NAMES

#todo: change loction of hunchly case



ENTITIES_TYPE_NAMES.register(name='CASE', item='cnd.HunchlyCase')
ENTITIES_TYPE_NAMES.register(name='PAGE', item='cnd.Webpage')
ENTITIES_TYPE_NAMES.register(name='EMAIL', item='cnd.Email')
ENTITIES_TYPE_NAMES.register(name='IPV4', item='cnd.IPV4')
ENTITIES_TYPE_NAMES.register(name='IPV6', item='cnd.IPV6')
ENTITIES_TYPE_NAMES.register(name='GOOGLE_ANALYTICS', item='cnd.GoogleAnalytics')
ENTITIES_TYPE_NAMES.register(name='FACEBOOK_PIXEL', item='cnd.FacebookPixel')
ENTITIES_TYPE_NAMES.register(name='TOR_SERVICE', item='cnd.TorService')
ENTITIES_TYPE_NAMES.register(name='SOCIAL_MEDIA_ACCOUNT', item='cnd.SocialMediaAccount')
ENTITIES_TYPE_NAMES.register(name='PHOTO', item='cnd.Image')
ENTITIES_TYPE_NAMES.register(name='SELECTOR', item='cnd.Selector')
ENTITIES_TYPE_NAMES.register(name='TAG', item='cnd.Tag')
ENTITIES_TYPE_NAMES.register(name='USERNAME', item='cnd.Username')
ENTITIES_TYPE_NAMES.register(name='ALIAS', item='cnd.Alias')
ENTITIES_TYPE_NAMES.register(name='CLOAK_N_DAGGER', item='cnd.CloakNDagger')
ENTITIES_TYPE_NAMES.register(name='TEXT', item='cnd.Text')
ENTITIES_TYPE_NAMES.register(name='TAVILY', item='cnd.Tavily')


class Case(BaseEntity):
    setting: EntitySetting = Field(default=EntitySetting(type=ENTITIES_TYPE_NAMES.CASE,
                                                         main_attribute='name',
                                                         match='strict'))
    id: int = Field(default=0)
    name: str = Field(default='')


class Page(BaseEntity, extra='allow'):
    setting: EntitySetting = Field(default=EntitySetting(type=ENTITIES_TYPE_NAMES.PAGE,
                                                         main_attribute='title',
                                                         match='strict'))
    url: AnyUrl
    title: str
    icon: str = WEBPAGE


class Email(BaseEntity):
    setting: EntitySetting = Field(default=EntitySetting(type=ENTITIES_TYPE_NAMES.EMAIL,
                                                         main_attribute='email',
                                                         match='strict'))
    icon: str = EMAIL
    email: str


class IPV4(BaseEntity):
    setting: EntitySetting = Field(default=EntitySetting(type=ENTITIES_TYPE_NAMES.IPV4,
                                                         main_attribute='ipv4',
                                                         match='strict'))
    icon: str = IP
    ipv4: str = Field(validation_alias='data_record')


class IPV6(BaseEntity):
    setting: EntitySetting = Field(default=EntitySetting(type=ENTITIES_TYPE_NAMES.IPV6,
                                                         main_attribute='ipv6',
                                                         match='strict'))
    icon: str = IP
    ipv6: str


class GoogleAnalytics(BaseEntity):
    setting: EntitySetting = Field(default=EntitySetting(type=ENTITIES_TYPE_NAMES.GOOGLE_ANALYTICS,
                                                         main_attribute='id',
                                                         match='strict'))
    id: str
    icon: str = IDENTIFICATOR


class FacebookPixel(BaseEntity):
    setting: EntitySetting = Field(default=EntitySetting(type=ENTITIES_TYPE_NAMES.FACEBOOK_PIXEL,
                                                         main_attribute='id',
                                                         match='strict'))
    id: str
    icon: str = IDENTIFICATOR


class TorService(BaseEntity):
    setting: EntitySetting = Field(default=EntitySetting(type=ENTITIES_TYPE_NAMES.TOR_SERVICE,
                                                         main_attribute='url',
                                                         match='strict'))
    url: str


class SocialMediaProfile(BaseEntity):
    setting: EntitySetting = Field(default=EntitySetting(type=ENTITIES_TYPE_NAMES.SOCIAL_MEDIA_ACCOUNT,
                                                         main_attribute='url',
                                                         match='strict'))
    url: str
    icon: str = WEB_PROFILE


class Photo(BaseEntity):
    """
    url     - location on net
    path    - location on file system
    """
    setting: EntitySetting = Field(default=EntitySetting(type=ENTITIES_TYPE_NAMES.PHOTO,
                                                         main_attribute='name',
                                                         match='strict'))
    hash: str = Field(default='')
    url: str = Field(default='')
    path: str = Field(default='')
    name: str = Field(default='')
    icon: str = IMAGE


class Selector(BaseEntity):
    setting: EntitySetting = Field(default=EntitySetting(type=ENTITIES_TYPE_NAMES.SELECTOR,
                                                         main_attribute='name',
                                                         match='strict'))
    name: str
    icon: str = TARGET


class Tag(BaseEntity):
    setting: EntitySetting = Field(default=EntitySetting(type=ENTITIES_TYPE_NAMES.TAG,
                                                         main_attribute='name',
                                                         match='strict'))
    name: str
    icon: str = TAG


class Username(BaseEntity):
    setting: EntitySetting = Field(default=EntitySetting(type=ENTITIES_TYPE_NAMES.USERNAME,
                                                         main_attribute='username',
                                                         match='strict'))
    username: str


class Alias(BaseEntity):
    setting: EntitySetting = Field(default=EntitySetting(type=ENTITIES_TYPE_NAMES.ALIAS,
                                                         main_attribute='alias',
                                                         match='strict'))
    alias: str = Field(default='')


class CloakNDagger(BaseEntity):
    setting: EntitySetting = Field(default=EntitySetting(type=ENTITIES_TYPE_NAMES.CLOAK_N_DAGGER,
                                                         main_attribute='moto',
                                                         match='strict'))
    moto: str


class Text(BaseEntity):
    setting: EntitySetting = Field(default=EntitySetting(type=ENTITIES_TYPE_NAMES.TEXT,
                                                         main_attribute='text',
                                                         match='strict'))
    text: str = Field(default='')
    icon: str = COMMENT

    @model_validator(mode='before')
    @classmethod
    def set_note(cls, data):
        data['note'] = data['text']
        return data




entity_register.register(name=ENTITIES_TYPE_NAMES.CASE, item=Case)
entity_register.register(name=ENTITIES_TYPE_NAMES.PAGE, item=Page)
entity_register.register(name=ENTITIES_TYPE_NAMES.EMAIL, item=EMAIL)
entity_register.register(name=ENTITIES_TYPE_NAMES.IPV4, item=IPV4)
entity_register.register(name=ENTITIES_TYPE_NAMES.IPV6, item=IPV6)
entity_register.register(name=ENTITIES_TYPE_NAMES.GOOGLE_ANALYTICS, item=GoogleAnalytics)
entity_register.register(name=ENTITIES_TYPE_NAMES.FACEBOOK_PIXEL, item=FacebookPixel)
entity_register.register(name=ENTITIES_TYPE_NAMES.TOR_SERVICE, item=TorService)
entity_register.register(name=ENTITIES_TYPE_NAMES.SOCIAL_MEDIA_ACCOUNT, item=SocialMediaProfile)
entity_register.register(name=ENTITIES_TYPE_NAMES.PHOTO, item=Photo)
entity_register.register(name=ENTITIES_TYPE_NAMES.SELECTOR, item=Selector)
entity_register.register(name=ENTITIES_TYPE_NAMES.TAG, item=Tag)
entity_register.register(name=ENTITIES_TYPE_NAMES.USERNAME, item=Username)
entity_register.register(name=ENTITIES_TYPE_NAMES.ALIAS, item=Alias)
entity_register.register(name=ENTITIES_TYPE_NAMES.CLOAK_N_DAGGER, item=CloakNDagger)
entity_register.register(name=ENTITIES_TYPE_NAMES.TEXT, item=Text)