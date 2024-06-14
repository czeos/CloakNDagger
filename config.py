from abc import ABC
from typing import Literal, Union
from pathlib import Path
from pydantic import BaseModel, Field, field_validator

from tools.utils import load_toml
from tools.base import BaseRegisterFactory

BASE_PATH = Path(__file__).resolve().parent

class CND(BaseModel):
    debug: bool = Field(default=True, description='Set debug mode')
    community: bool = Field(default=True, description='Is community')


class Database(BaseModel, ABC):
    type: str


class TinyDB(Database):
    type: Literal['tinydb', 'tinyDB']
    db_path: Path

    @field_validator('db_path')
    @classmethod
    def set_path(cls, value) -> Path:
        return BASE_PATH / value


database_register = BaseRegisterFactory()
database_register.register('tinydb', TinyDB)


class Hunchly(BaseModel):
    api_path: str


class Whatsmynmeapp(BaseModel):
    data: str


class Tavily(BaseModel):
    api_key: str = Field(default='')


class Config(BaseModel):
    cnd: CND
    db: Union[TinyDB]
    hunchly: Hunchly
    whatsmynmeapp: Whatsmynmeapp
    tavily: Tavily


config = Config(**load_toml(BASE_PATH / 'config.toml'))

if __name__ == '__main__':
    pass