from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from schemas import KategorijaCreate, KategorijaOut
from crud import kategorije

router = APIRouter(prefix="/kategorije", tags=["Kategorije"])

@router.post("/", response_model=KategorijaOut)
def create_kategorija(kategorija_data: KategorijaCreate, db: Session = Depends(get_db)):
    return kategorije.create_kategorija(db, kategorija_data)

@router.get("/", response_model=list[KategorijaOut])
def list_kategorije(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return kategorije.get_kategorije(db, skip, limit)

@router.get("/{kategorija_id}", response_model=KategorijaOut)
def read_kategorija(kategorija_id: int, db: Session = Depends(get_db)):
    kategorija = kategorije.get_kategorija(db, kategorija_id)
    if not kategorija:
        raise HTTPException(status_code=404, detail="Kategorija nije pronađena")
    return kategorija

@router.put("/{kategorija_id}", response_model=KategorijaOut)
def update_kategorija(kategorija_id: int, kategorija_data: KategorijaCreate, db: Session = Depends(get_db)):
    return kategorije.update_kategorija(db, kategorija_id, kategorija_data.dict())

@router.delete("/{kategorija_id}")
def delete_kategorija(kategorija_id: int, db: Session = Depends(get_db)):
    kategorija = kategorije.delete_kategorija(db, kategorija_id)
    if not kategorija:
        raise HTTPException(status_code=404, detail="Kategorija nije pronađena")
    return {"detail": "Kategorija obrisana"}
