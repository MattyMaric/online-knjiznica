from sqlalchemy import (
    Column, Float, Integer, String, Boolean, Date, ForeignKey, Numeric, Text, DateTime
)
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime

Base = declarative_base()

# ------------------- KORISNIK -------------------
class Korisnik(Base):
    __tablename__ = "korisnik"

    id = Column(Integer, primary_key=True)
    korisnicko_ime = Column(String, unique=True, nullable=False)
    ime = Column(String, nullable=False)
    prezime = Column(String, nullable=False)
    datum_rodenja = Column(Date, nullable=False)
    spol = Column(String, nullable=False)  # 'M' ili 'Ž'
    adresa = Column(String)
    email = Column(String, nullable=True)
    broj_mobitela = Column(String)
    lozinka = Column(String, nullable=False)  # hashed
    admin = Column(Boolean, default=False)

    # Relationships
    korpa = relationship("Korpa", back_populates="korisnik", cascade="all, delete")
    lista_zelja = relationship("ListaZelja", back_populates="korisnik", cascade="all, delete")
    posudbe = relationship("Posudba", back_populates="korisnik", cascade="all, delete")
    narudzbe = relationship("Narudzba", back_populates="korisnik", cascade="all, delete")
    recenzije = relationship("Recenzija", back_populates="korisnik", cascade="all, delete")

 
# ------------------- KATEGORIJA -------------------
class Kategorija(Base):
    __tablename__ = "kategorija"

    id = Column(Integer, primary_key=True)
    naziv = Column(String, unique=True, nullable=False)

    knjige = relationship("Knjiga", back_populates="kategorija", cascade="all, delete")


# ------------------- KNJIGA -------------------
class Knjiga(Base):
    __tablename__ = "knjiga"

    id = Column(Integer, primary_key=True, index=True)
    naziv_djela = Column(String, nullable=False)
    autor = Column(String)
    opis = Column(String)
    cijena = Column(Float, nullable=False)
    cijena15 = Column(Float, nullable=True) 
    cijena30 = Column(Float, nullable=True) 
    stanje = Column(Integer)
    slika_url = Column(String, nullable=True)  # polje za URL slike ili putanju do slike

    kategorija_id = Column(Integer, ForeignKey("kategorija.id"))

    # Relationships
    kategorija = relationship("Kategorija", back_populates="knjige")
    korpa = relationship("Korpa", back_populates="knjiga", cascade="all, delete")
    lista_zelja = relationship("ListaZelja", back_populates="knjiga", cascade="all, delete")
    posudbe = relationship("Posudba", back_populates="knjiga", cascade="all, delete")
    recenzije = relationship("Recenzija", back_populates="knjiga", cascade="all, delete")
    narudzba_stavke = relationship("NarudzbaStavka", back_populates="knjiga", cascade="all, delete")


# ------------------- KORPA -------------------
class Korpa(Base):
    __tablename__ = "korpa"

    id = Column(Integer, primary_key=True, index=True)
    korisnik_id = Column(Integer, ForeignKey("korisnik.id"))
    knjiga_id = Column(Integer, ForeignKey("knjiga.id"))
    tip = Column(Integer, nullable=False)  # <-- OVO MORA POSTOJATI!

    korisnik = relationship("Korisnik", back_populates="korpa")
    knjiga = relationship("Knjiga", back_populates="korpa")


# ------------------- LISTA ŽELJA -------------------
class ListaZelja(Base):
    __tablename__ = "lista_zelja"

    id = Column(Integer, primary_key=True)
    korisnik_id = Column(Integer, ForeignKey("korisnik.id"))
    knjiga_id = Column(Integer, ForeignKey("knjiga.id"))

    korisnik = relationship("Korisnik", back_populates="lista_zelja")
    knjiga = relationship("Knjiga", back_populates="lista_zelja")


# ------------------- POSUDBA -------------------
class Posudba(Base):
    __tablename__ = "posudba"

    id = Column(Integer, primary_key=True)
    korisnik_id = Column(Integer, ForeignKey("korisnik.id"))
    knjiga_id = Column(Integer, ForeignKey("knjiga.id"))
    datum_posudbe = Column(DateTime, default=datetime.utcnow)
    rok_vracanja = Column(DateTime)

    korisnik = relationship("Korisnik", back_populates="posudbe")
    knjiga = relationship("Knjiga", back_populates="posudbe")


# ------------------- NARUDŽBA -------------------
class Narudzba(Base):
    __tablename__ = "narudzba"

    id = Column(Integer, primary_key=True)
    korisnik_id = Column(Integer, ForeignKey("korisnik.id"))
    datum_narudzbe = Column(DateTime, default=datetime.utcnow)

    korisnik = relationship("Korisnik", back_populates="narudzbe")
    stavke = relationship("NarudzbaStavka", back_populates="narudzba", cascade="all, delete")


class NarudzbaStavka(Base):
    __tablename__ = "narudzba_stavka"

    id = Column(Integer, primary_key=True)
    narudzba_id = Column(Integer, ForeignKey("narudzba.id"))
    knjiga_id = Column(Integer, ForeignKey("knjiga.id"))
    kolicina = Column(Integer, default=1)

    narudzba = relationship("Narudzba", back_populates="stavke")
    knjiga = relationship("Knjiga", back_populates="narudzba_stavke")


# ------------------- RECENZIJA -------------------
class Recenzija(Base):
    __tablename__ = "recenzija"

    id = Column(Integer, primary_key=True)
    korisnik_id = Column(Integer, ForeignKey("korisnik.id"))
    knjiga_id = Column(Integer, ForeignKey("knjiga.id"))
    ocjena = Column(Integer)  # 1 to 5
    komentar = Column(Text)
    datum = Column(DateTime, default=datetime.utcnow)

    korisnik = relationship("Korisnik", back_populates="recenzije")
    knjiga = relationship("Knjiga", back_populates="recenzije")
