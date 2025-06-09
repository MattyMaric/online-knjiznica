from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from schemas import PosudbaCreate, PosudbaOut
from crud import posudbe

router = APIRouter(prefix="/posudbe", tags=["Posudbe"])

@router.post("/", response_model=PosudbaOut)
def create_posudba(posudba_data: PosudbaCreate, db: Session = Depends(get_db)):
    return posudbe.create_posudba(db, posudba_data)

@router.get("/", response_model=list[PosudbaOut])
def list_posudbe(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return posudbe.get_posudbe(db, skip, limit)

@router.get("/{posudba_id}", response_model=PosudbaOut)
def read_posudba(posudba_id: int, db: Session = Depends(get_db)):
    posudba = posudbe.get_posudba(db, posudba_id)
    if not posudba:
        raise HTTPException(status_code=404, detail="Posudba nije pronađena")
    return posudba

@router.put("/{posudba_id}", response_model=PosudbaOut)
def update_posudba(posudba_id: int, posudba_data: PosudbaCreate, db: Session = Depends(get_db)):
    return posudbe.update_posudba(db, posudba_id, posudba_data.dict())

@router.delete("/{posudba_id}")
def delete_posudba(posudba_id: int, db: Session = Depends(get_db)):
    posudba = posudbe.delete_posudba(db, posudba_id)
    if not posudba:
        raise HTTPException(status_code=404, detail="Posudba nije pronađena")
    return {"detail": "Posudba obrisana"}
