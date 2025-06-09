from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from schemas import NarudzbaCreate, NarudzbaOut
from crud import narudzbe

router = APIRouter(prefix="/narudzbe", tags=["Narudzbe"])

@router.post("/", response_model=NarudzbaOut)
def create_narudzba(narudzba_data: NarudzbaCreate, db: Session = Depends(get_db)):
    return narudzbe.create_narudzba(db, narudzba_data)

@router.get("/", response_model=list[NarudzbaOut])
def list_narudzbe(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return narudzbe.get_narudzbe(db, skip, limit)

@router.get("/{narudzba_id}", response_model=NarudzbaOut)
def read_narudzba(narudzba_id: int, db: Session = Depends(get_db)):
    narudzba = narudzbe.get_narudzba(db, narudzba_id)
    if not narudzba:
        raise HTTPException(status_code=404, detail="Narudžba nije pronađena")
    return narudzba

@router.delete("/{narudzba_id}")
def delete_narudzba(narudzba_id: int, db: Session = Depends(get_db)):
    narudzba = narudzbe.delete_narudzba(db, narudzba_id)
    if not narudzba:
        raise HTTPException(status_code=404, detail="Narudžba nije pronađena")
    return {"detail": "Narudžba obrisana"}
