from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from schemas import KorpaCreate, KorpaOut
from crud import korpa

router = APIRouter(prefix="/korpa", tags=["Korpa"])

@router.post("/", response_model=KorpaOut)
def add_item_to_korpa(korpa_data: KorpaCreate, db: Session = Depends(get_db)):
    return korpa.add_to_korpa(db, korpa_data)

@router.get("/{korisnik_id}", response_model=list[KorpaOut])
def get_korpa(korisnik_id: int, db: Session = Depends(get_db)):
    return korpa.get_korpa_by_user(db, korisnik_id)

@router.delete("/{korpa_id}")
def delete_korpa_item(korpa_id: int, db: Session = Depends(get_db)):
    item = korpa.remove_from_korpa(db, korpa_id)
    if not item:
        raise HTTPException(status_code=404, detail="Stavka u korpi nije pronađena")
    return {"detail": "Stavka iz korpe obrisana"}
