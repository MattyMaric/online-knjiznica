from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel

class KnjigaBase(BaseModel):
    naziv: str
    autor: str
    kategorija_id: int
    cijena: float
    stanje: str

class KnjigaCreate(KnjigaBase):
    pass

class KnjigaOut(KnjigaBase):
    id: int
    class Config:
        orm_mode = True

#Korisnici
class KorisnikBase(BaseModel):
    ime: str
    prezime: str
    datum_rodenja: date
    spol: str
    email: Optional[str] = None
    adresa: str
    broj_mobitela: str
    admin: bool = False

class KorisnikCreate(KorisnikBase):
    lozinka: str  # plain text, hashamo u bazi

class KorisnikOut(KorisnikBase):
    id: int
    class Config:
        orm_mode = True

#Kategorije
class KategorijaBase(BaseModel):
    naziv: str

class KategorijaCreate(KategorijaBase):
    pass

class KategorijaOut(KategorijaBase):
    id: int
    class Config:
        orm_mode = True

#Korpa
class KorpaBase(BaseModel):
    korisnik_id: int
    knjiga_id: int

class KorpaCreate(KorpaBase):
    pass

class KorpaOut(KorpaBase):
    id: int
    class Config:
        orm_mode = True

#wishlist
class ListaZeljaBase(BaseModel):
    korisnik_id: int
    knjiga_id: int

class ListaZeljaCreate(ListaZeljaBase):
    pass

class ListaZeljaOut(ListaZeljaBase):
    id: int
    class Config:
        orm_mode = True

#posudba
class PosudbaBase(BaseModel):
    korisnik_id: int
    knjiga_id: int
    datum_posudbe: Optional[datetime] = None
    datum_vracanja: Optional[datetime] = None

class PosudbaCreate(PosudbaBase):
    pass

class PosudbaOut(PosudbaBase):
    id: int
    class Config:
        orm_mode = True

#narudzba
class NarudzbaBase(BaseModel):
    korisnik_id: int
    ukupna_cijena: float

class NarudzbaCreate(NarudzbaBase):
    pass

class NarudzbaOut(NarudzbaBase):
    id: int
    datum_narudzbe: Optional[datetime]

    class Config:
        orm_mode = True

#Recenzija
class RecenzijaBase(BaseModel):
    korisnik_id: int
    knjiga_id: int
    ocjena: int
    komentar: Optional[str] = None

class RecenzijaCreate(RecenzijaBase):
    pass

class RecenzijaOut(RecenzijaBase):
    id: int
    datum_objave: Optional[datetime]

    class Config:
        orm_mode = True