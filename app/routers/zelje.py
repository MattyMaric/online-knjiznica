from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from schemas import ListaZeljaCreate, ListaZeljaOut
from crud import lista_zelja

router = APIRouter(prefix="/lista-zelja", tags=["Lista želja"])

@router.post("/", response_model=ListaZeljaOut)
def add_item_to_lista_zelja(zelja_data: ListaZeljaCreate, db: Session = Depends(get_db)):
    return lista_zelja.add_to_lista_zelja(db, zelja_data)

@router.get("/{korisnik_id}", response_model=list[ListaZeljaOut])
def get_lista_zelja(korisnik_id: int, db: Session = Depends(get_db)):
    return lista_zelja.get_lista_zelja_by_user(db, korisnik_id)

@router.delete("/{zelja_id}")
def delete_lista_zelja_item(zelja_id: int, db: Session = Depends(get_db)):
    item = lista_zelja.remove_from_lista_zelja(db, zelja_id)
    if not item:
        raise HTTPException(status_code=404, detail="Stavka na listi želja nije pronađena")
    return {"detail": "Stavka sa liste želja obrisana"}
