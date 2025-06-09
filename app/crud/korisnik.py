from sqlalchemy.orm import Session
from app import models
from app.schemas import KorisnikCreate
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

def create_korisnik(db: Session, korisnik: KorisnikCreate):
    hashed_password = get_password_hash(korisnik.lozinka)
    db_korisnik = models.Korisnik(
        ime=korisnik.ime,
        prezime=korisnik.prezime,
        datum_rodenja=korisnik.datum_rodenja,
        spol=korisnik.spol,
        adresa=korisnik.adresa,
        broj_mobitela=korisnik.broj_mobitela,
        lozinka=hashed_password,
        admin=korisnik.admin,
    )
    db.add(db_korisnik)
    db.commit()
    db.refresh(db_korisnik)
    return db_korisnik

def get_korisnici(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Korisnik).offset(skip).limit(limit).all()

def get_korisnik(db: Session, korisnik_id: int):
    return db.query(models.Korisnik).filter(models.Korisnik.id == korisnik_id).first()

def update_korisnik(db: Session, korisnik_id: int, data: dict):
    korisnik = db.query(models.Korisnik).filter(models.Korisnik.id == korisnik_id).first()
    if korisnik:
        for key, value in data.items():
            if key == "lozinka":
                value = get_password_hash(value)
            setattr(korisnik, key, value)
        db.commit()
        db.refresh(korisnik)
    return korisnik

def delete_korisnik(db: Session, korisnik_id: int):
    korisnik = db.query(models.Korisnik).filter(models.Korisnik.id == korisnik_id).first()
    if korisnik:
        db.delete(korisnik)
        db.commit()
    return korisnik
