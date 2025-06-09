from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from schemas import KorisnikCreate, KorisnikOut
from crud import korisnici

router = APIRouter(prefix="/korisnici", tags=["Korisnici"])

@router.post("/", response_model=KorisnikOut)
def create_korisnik(korisnik_data: KorisnikCreate, db: Session = Depends(get_db)):
    return korisnici.create_korisnik(db, korisnik_data)

@router.get("/", response_model=list[KorisnikOut])
def list_korisnici(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return korisnici.get_korisnici(db, skip, limit)

@router.get("/{korisnik_id}", response_model=KorisnikOut)
def read_korisnik(korisnik_id: int, db: Session = Depends(get_db)):
    korisnik = korisnici.get_korisnik(db, korisnik_id)
    if not korisnik:
        raise HTTPException(status_code=404, detail="Korisnik nije pronađen")
    return korisnik

@router.put("/{korisnik_id}", response_model=KorisnikOut)
def update_korisnik(korisnik_id: int, korisnik_data: KorisnikCreate, db: Session = Depends(get_db)):
    return korisnici.update_korisnik(db, korisnik_id, korisnik_data.dict())

@router.delete("/{korisnik_id}")
def delete_korisnik(korisnik_id: int, db: Session = Depends(get_db)):
    korisnik = korisnici.delete_korisnik(db, korisnik_id)
    if not korisnik:
        raise HTTPException(status_code=404, detail="Korisnik nije pronađen")
    return {"detail": "Korisnik obrisan"}
