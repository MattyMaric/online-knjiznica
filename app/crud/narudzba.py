from sqlalchemy.orm import Session
from app.models import Narudzba
from app.schemas import NarudzbaCreate
import datetime

def create_narudzba(db: Session, narudzba: NarudzbaCreate):
    db_narudzba = Narudzba(
        korisnik_id=narudzba.korisnik_id,
        ukupna_cijena=narudzba.ukupna_cijena,
        datum_narudzbe=datetime.datetime.utcnow()
    )
    db.add(db_narudzba)
    db.commit()
    db.refresh(db_narudzba)
    return db_narudzba

def get_narudzbe(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Narudzba).offset(skip).limit(limit).all()

def get_narudzba(db: Session, narudzba_id: int):
    return db.query(Narudzba).filter(Narudzba.id == narudzba_id).first()

def delete_narudzba(db: Session, narudzba_id: int):
    narudzba = db.query(Narudzba).filter(Narudzba.id == narudzba_id).first()
    if narudzba:
        db.delete(narudzba)
        db.commit()
    return narudzba
