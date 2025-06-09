from sqlalchemy.orm import Session
from models import Kategorija, Knjiga
from schemas import KnjigaCreate

def create_knjiga(db: Session, knjiga: KnjigaCreate):
    db_knjiga = Knjiga(**knjiga.dict())
    db.add(db_knjiga)
    db.commit()
    db.refresh(db_knjiga)
    return db_knjiga

def get_knjige(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Knjiga).offset(skip).limit(limit).all()

def get_knjiga(db: Session, knjiga_id: int):
    return db.query(Knjiga).filter(Knjiga.id == knjiga_id).first()

def update_knjiga(db: Session, knjiga_id: int, knjiga_data: dict):
    knjiga = db.query(Knjiga).filter(Knjiga.id == knjiga_id).first()
    if knjiga:
        for key, value in knjiga_data.items():
            setattr(knjiga, key, value)
        db.commit()
        db.refresh(knjiga)
    return knjiga

def delete_knjiga(db: Session, knjiga_id: int):
    knjiga = db.query(Knjiga).filter(Knjiga.id == knjiga_id).first()
    if knjiga:
        db.delete(knjiga)
        db.commit()
    return knjiga


def dohvati_knjige(db: Session):
    return db.query(Knjiga).all()

def dohvati_kategorije(db):
    return db.query(Kategorija).all()

def get_books_by_kategorija(db: Session, kategorija_id: int):
    return db.query(Knjiga).filter(Knjiga.kategorija_id == kategorija_id).all()

def dohvati_sve_kategorije(db: Session):
    return db.query(Kategorija).all()