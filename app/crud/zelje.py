from sqlalchemy.orm import Session
from app.models import ListaZelja
from app.schemas import ListaZeljaCreate

def add_to_lista_zelja(db: Session, zelja: ListaZeljaCreate):
    db_zelja = ListaZelja(**zelja.dict())
    db.add(db_zelja)
    db.commit()
    db.refresh(db_zelja)
    return db_zelja

def get_lista_zelja_by_user(db: Session, korisnik_id: int):
    return db.query(ListaZelja).filter(ListaZelja.korisnik_id == korisnik_id).all()

def remove_from_lista_zelja(db: Session, zelja_id: int):
    zelja = db.query(ListaZelja).filter(ListaZelja.id == zelja_id).first()
    if zelja:
        db.delete(zelja)
        db.commit()
    return zelja
