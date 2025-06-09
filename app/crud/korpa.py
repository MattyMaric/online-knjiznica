from sqlalchemy.orm import Session
from app.models import Korpa
from app.schemas import KorpaCreate

def add_to_korpa(db: Session, korpa_item: KorpaCreate):
    db_item = Korpa(**korpa_item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def get_korpa_by_user(db: Session, korisnik_id: int):
    return db.query(Korpa).filter(Korpa.korisnik_id == korisnik_id).all()

def remove_from_korpa(db: Session, korpa_id: int):
    korpa_item = db.query(Korpa).filter(Korpa.id == korpa_id).first()
    if korpa_item:
        db.delete(korpa_item)
        db.commit()
    return korpa_item