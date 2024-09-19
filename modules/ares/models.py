from tools.entities import Company,Person
from pydantic import BaseModel, Field
from typing import List, Literal,Optional, Union

#todo: add entities add forma
#todo: response entity website> aka

class Sidlo(BaseModel):
    cisloDomovni: int = None
    cisloOrientacni: int = None
    cisloOrientacniPismeno: str = None
    textovaAdresa: str = None
    nazevStatu: str = None

class RequestEkonomickySubjekt(BaseModel):
    start : int = 0
    pocet: int = 10
    ico: Optional[List[str]] = None
    obchodniJmeno: str = Field(validation_alias ='name')
    sidlo: Optional[Sidlo] = None

class AdresaDorucovaci(BaseModel):
    radekAdresy1: str = None
    radekAdresy2: str = None
    radekAdresy3: str= None

class SeznamRegistraci(BaseModel):
    stavZdrojeVr: str
    stavZdrojeRes: str
    stavZdrojeRzp: str
    stavZdrojeNrpzs: str
    stavZdrojeRpsh: str
    stavZdrojeRcns: str
    stavZdrojeSzr: str
    stavZdrojeDph: str
    stavZdrojeSd: str
    stavZdrojeIr: str
    stavZdrojeCeu: str
    stavZdrojeRs: str
    stavZdrojeRed: str
    stavZdrojeMonitor: str

class ObchodniJmeno(BaseModel):
    obchodniJmeno: str
    primarniZaznam: bool

class DalsiUdaje(BaseModel):
    obchodniJmeno: List[ObchodniJmeno]
    sidlo: List[Sidlo]
    pravniForma: str
    datovyZdroj: str

class EkonomickySubjekt(BaseModel):
    ico: str = None
    obchodniJmeno: str = None
    sidlo: Sidlo = None 
    pravniForma: str = None
    financniUrad: str = None
    datumVzniku: str = None
    datumAktualizace: str = None
    dic: str = None
    icoId: str = None
    adresaDorucovaci: AdresaDorucovaci = None
    seznamRegistraci: SeznamRegistraci = None
    primarniZdroj: str = None
    dalsiUdaje: List[DalsiUdaje] = None
    czNace: List[str] = None
    subRegistrSzr: str = None

class PravnickaOsoba(Company,EkonomickySubjekt):
    name: str = Field(validation_alias='obchodniJmeno')
    pravniForma: Literal[
    '111', '112', '113', '115', '116', '117',
    '121', '141', '124',
    '141', '142', '144', '148', '149',
    '201', '205', '301', '302', '303', '304', '308', '311',
    '331', '332',
    '601', '602', '603',
    '706',
    '911', '931', '932'
]

class FyzickaOsoba(Person,EkonomickySubjekt):
    fullname: str = Field(validation_alias='obchodniJmeno')
    pravniForma: Literal['101', '102', '105','106','107','108','109','110']

class Root(BaseModel):
    pocetCelkem: int
    ekonomickeSubjekty: List[Union[PravnickaOsoba,FyzickaOsoba]]
