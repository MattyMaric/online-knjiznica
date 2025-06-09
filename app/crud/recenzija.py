from sqlalchemy.orm import Session
from app.models import Recenzija
from app.schemas import RecenzijaCreate
import datetime

def create_recenzija(db: Session, recenzija: RecenzijaCreate):
    db_recenzija = Recenzija(**recenzija.dict())
    db.add(db_recenzija)
    db.commit()
    db.refresh(db_recenzija)
    return db_recenzija

def get_recenzije(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Recenzija).offset(skip).limit(limit).all()

def get_recenzija(db: Session, recenzija_id: int):
    return db.query(Recenzija).filter(Recenzija.id == recenzija_id).first()

def get_recenzije_by_knjiga(db: Session, knjiga_id: int):
    return db.query(Recenzija).filter(Recenzija.knjiga_id == knjiga_id).all()

def update_recenzija(db: Session, recenzija_id: int, data: dict):
    recenzija = db.query(Recenzija).filter(Recenzija.id == recenzija_id).first()
    if recenzija:
        for key, value in data.items():
            setattr(recenzija, key, value)
        db.commit()
        db.refresh(recenzija)
    return recenzija

def delete_recenzija(db: Session, recenzija_id: int):
    recenzija = db.query(Recenzija).filter(Recenzija.id == recenzija_id).first()
    if recenzija:
        db.delete(recenzija)
        db.commit()
    return recenzija
