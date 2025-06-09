from sqlalchemy.orm import Session
from app.models import Posudba
from app.schemas import PosudbaCreate
import datetime

def create_posudba(db: Session, posudba: PosudbaCreate):
    if not posudba.datum_posudbe:
        posudba.datum_posudbe = datetime.datetime.utcnow()
    db_posudba = Posudba(**posudba.dict())
    db.add(db_posudba)
    db.commit()
    db.refresh(db_posudba)
    return db_posudba

def get_posudbe(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Posudba).offset(skip).limit(limit).all()

def get_posudba(db: Session, posudba_id: int):
    return db.query(Posudba).filter(Posudba.id == posudba_id).first()

def update_posudba(db: Session, posudba_id: int, data: dict):
    posudba = db.query(Posudba).filter(Posudba.id == posudba_id).first()
    if posudba:
        for key, value in data.items():
            setattr(posudba, key, value)
        db.commit()
        db.refresh(posudba)
    return posudba

def delete_posudba(db: Session, posudba_id: int):
    posudba = db.query(Posudba).filter(Posudba.id == posudba_id).first()
    if posudba:
        db.delete(posudba)
        db.commit()
    return posudba
