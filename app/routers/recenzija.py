from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from schemas import RecenzijaCreate, RecenzijaOut
from crud import recenzije

router = APIRouter(prefix="/recenzije", tags=["Recenzije"])

@router.post("/", response_model=RecenzijaOut)
def create_recenzija(recenzija_data: RecenzijaCreate, db: Session = Depends(get_db)):
    return recenzije.create_recenzija(db, recenzija_data)

@router.get("/", response_model=list[RecenzijaOut])
def list_recenzije(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return recenzije.get_recenzije(db, skip, limit)

@router.get("/{recenzija_id}", response_model=RecenzijaOut)
def read_recenzija(recenzija_id: int, db: Session = Depends(get_db)):
    recenzija = recenzije.get_recenzija(db, recenzija_id)
    if not recenzija:
        raise HTTPException(status_code=404, detail="Recenzija nije pronađena")
    return recenzija

@router.get("/knjiga/{knjiga_id}", response_model=list[RecenzijaOut])
def get_recenzije_knjiga(knjiga_id: int, db: Session = Depends(get_db)):
    return recenzije.get_recenzije_by_knjiga(db, knjiga_id)

@router.put("/{recenzija_id}", response_model=RecenzijaOut)
def update_recenzija(recenzija_id: int, recenzija_data: RecenzijaCreate, db: Session = Depends(get_db)):
    rec = recenzije.update_recenzija(db, recenzija_id, recenzija_data.dict())
    if not rec:
        raise HTTPException(status_code=404, detail="Recenzija nije pronađena")
    return rec

@router.delete("/{recenzija_id}")
def delete_recenzija(recenzija_id: int, db: Session = Depends(get_db)):
    rec = recenzije.delete_recenzija(db, recenzija_id)
    if not rec:
        raise HTTPException(status_code=404, detail="Recenzija nije pronađena")
    return {"detail": "Recenzija obrisana"}
