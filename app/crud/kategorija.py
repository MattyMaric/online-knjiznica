from sqlalchemy.orm import Session
from app.models import Kategorija
from app.schemas import KategorijaCreate

def create_kategorija(db: Session, kategorija: KategorijaCreate):
    db_kategorija = Kategorija(**kategorija.dict())
    db.add(db_kategorija)
    db.commit()
    db.refresh(db_kategorija)
    return db_kategorija

def get_kategorije(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Kategorija).offset(skip).limit(limit).all()

def get_kategorija(db: Session, kategorija_id: int):
    return db.query(Kategorija).filter(Kategorija.id == kategorija_id).first()

def update_kategorija(db: Session, kategorija_id: int, data: dict):
    kategorija = db.query(Kategorija).filter(Kategorija.id == kategorija_id).first()
    if kategorija:
        for key, value in data.items():
            setattr(kategorija, key, value)
        db.commit()
        db.refresh(kategorija)
    return kategorija

def delete_kategorija(db: Session, kategorija_id: int):
    kategorija = db.query(Kategorija).filter(Kategorija.id == kategorija_id).first()
    if kategorija:
        db.delete(kategorija)
        db.commit()
    return kategorija

def dohvati_sve_kategorije(db: Session):
    return db.query(Kategorija).all()