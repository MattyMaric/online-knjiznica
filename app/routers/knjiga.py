from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from crud import knjige
from schemas import KnjigaCreate, KnjigaOut

router = APIRouter(prefix="/knjige", tags=["Knjige"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=KnjigaOut)
def create_knjiga(knjiga_data: KnjigaCreate, db: Session = Depends(get_db)):
    return knjige.create_knjiga(db, knjiga_data)

@router.get("/", response_model=list[KnjigaOut])
def list_knjige(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return knjige.get_knjige(db, skip, limit)

@router.get("/{knjiga_id}", response_model=KnjigaOut)
def read_knjiga(knjiga_id: int, db: Session = Depends(get_db)):
    knjiga = knjige.get_knjiga(db, knjiga_id)
    if not knjiga:
        raise HTTPException(status_code=404, detail="Knjiga nije pronađena")
    return knjiga

@router.put("/{knjiga_id}", response_model=KnjigaOut)
def update_knjiga(knjiga_id: int, knjiga_data: KnjigaCreate, db: Session = Depends(get_db)):
    return knjige.update_knjiga(db, knjiga_id, knjiga_data.dict())

@router.delete("/{knjiga_id}")
def delete_knjiga(knjiga_id: int, db: Session = Depends(get_db)):
    knjiga = knjige.delete_knjiga(db, knjiga_id)
    if not knjiga:
        raise HTTPException(status_code=404, detail="Knjiga nije pronađena")
    return {"detail": "Knjiga obrisana"}
