from typing import Literal, Optional, Union
from pydantic import AliasChoices, BaseModel, Field
from tools.base import EntityDisplay
from tools.entities import Company, Person



class NodeData(BaseModel):
    id: str = Field(default=None)
    typeGroup: str = Field(default=None)
    ico: str = Field(default=None)
    address: str = Field(default=None)
    label: str = Field(default=None)
    url: str= Field(default=None)
    dateStart: Optional[str] = Field(default=None)
    dateEnd: Optional[str] = Field(default=None)

class PravnickaOsoba(Company,NodeData):
    name: str = Field(validation_alias='label')
    typeGroup: Literal['company']
    dateStartLogo: Optional[EntityDisplay] = None
    dateEndLogo: Optional[EntityDisplay] = None

class FyzickaOsoba(Person,NodeData):
    fullname: str = Field(validation_alias='label')    
    typeGroup: Literal['person']
    dateStartLogo: Optional[EntityDisplay] = None
    dateEndLogo: Optional[EntityDisplay] = None


class Node(BaseModel):
    data: Union[PravnickaOsoba,FyzickaOsoba] = Field(default=None)

class EdgeData(BaseModel):
    source: str = Field(default=None)
    target: str = Field(default=None)
    label: str = Field(default=None)
    dateStart: str = Field(default=None)
    dateEnd: Optional[str] = Field(default=None)

class Edge(BaseModel):
    data: EdgeData = Field(default=None)

class Root(BaseModel):
    nodes: list[Node] = Field(default=None)
    edges: list[Edge] = Field(default=None)


    