from fastapi import APIRouter, Request, Form, Depends, HTTPException, status
from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse
from passlib.context import CryptContext

from database import get_db
from models import Korisnik

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/login")
async def login_user(
    request: Request,
    korisnicko_ime: str = Form(...),
    lozinka: str = Form(...),
    db: Session = Depends(get_db)
):
    korisnik = db.query(Korisnik).filter(Korisnik.korisnicko_ime == korisnicko_ime).first()

    if not korisnik or not pwd_context.verify(lozinka, korisnik.lozinka):
        raise HTTPException(status_code=400, detail="Neispravno korisničko ime ili lozinka")

    # Spremanje podataka u sesiju
    request.session["korisnik_id"] = korisnik.id
    request.session["korisnicko_ime"] = korisnik.korisnicko_ime
    request.session["admin"] = korisnik.admin

    # Redirekcija ovisno o vrsti korisnika
    if korisnik.admin:
        return RedirectResponse(url="/admin", status_code=status.HTTP_302_FOUND)
    else:
        return RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
