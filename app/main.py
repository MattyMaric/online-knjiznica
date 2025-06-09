from datetime import date
from fastapi import FastAPI, Form, Request, Depends, Response
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from starlette.templating import Jinja2Templates
from routers import auth
from database import SessionLocal, engine, Base
from models import Korisnik
from starlette.middleware.sessions import SessionMiddleware
from crud.knjiga import dohvati_sve_kategorije, dohvati_knjige, get_books_by_kategorija


# Kreiraj tablice u bazi
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Mountaj static folder za CSS i HTML
app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(auth.router)

templates = Jinja2Templates(directory="static")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
app.add_middleware(SessionMiddleware, secret_key="tajna123")  

# Dependency za DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/register", response_class=HTMLResponse)
async def get_register(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@app.post("/register")
async def post_register(
    request: Request,
    korisnicko_ime: str = Form(...),
    lozinka: str = Form(...),
    ime: str = Form(None),
    prezime: str = Form(None),
    spol: str = Form(None),
    email: str = Form(None),
    adresa: str = Form(None),
    broj_mobitela: str = Form(None),
    datum_rodenja: date = Form(None),
    db: Session = Depends(get_db),
):
    # Provjeri postoji li korisnik
    user = db.query(Korisnik).filter(Korisnik.korisnicko_ime == korisnicko_ime).first()
    if user:
        return templates.TemplateResponse(
            "register.html",
            {"request": request, "error": "Korisničko ime je već zauzeto."},
        )
    
    hashed_password = pwd_context.hash(lozinka)

    novi_korisnik = Korisnik(
        korisnicko_ime=korisnicko_ime,
        lozinka=hashed_password,
        ime=ime,
        prezime=prezime,
        email=email,
        spol = spol,
        adresa=adresa,
        broj_mobitela=broj_mobitela,
        datum_rodenja=datum_rodenja,
        admin=False,
    )
    db.add(novi_korisnik)
    db.commit()
    db.refresh(novi_korisnik)


    return RedirectResponse(url="/login", status_code=303)

@app.get("/login", response_class=HTMLResponse)
def login_get(request: Request):
    user_id = request.session.get("user_id")  # <--- Ovdje promijeni
    if user_id:
        return RedirectResponse("/mojracun")
    return templates.TemplateResponse("login.html", {"request": request})


@app.post("/login")
def login_post(
    request: Request,
    korisnicko_ime: str = Form(...),
    lozinka: str = Form(...),
    db: Session = Depends(get_db)
):
    user = db.query(Korisnik).filter(Korisnik.korisnicko_ime == korisnicko_ime).first()
    if user and pwd_context.verify(lozinka, user.lozinka):
        request.session["user_id"] = user.id
        return RedirectResponse(url="/mojracun", status_code=303)
    return templates.TemplateResponse(
        "login.html",
        {"request": request, "error": "Neispravno korisničko ime ili lozinka."}
    )

@app.get("/", response_class=HTMLResponse)
def home(request: Request, db: Session = Depends(get_db)):
    user_id = request.session.get("user_id")  # <--- OVO je ispravno
    knjige = dohvati_knjige(db)
    return templates.TemplateResponse("index.html", {"request": request, "knjige": knjige})
                                      

@app.get("/kategorija", response_class=HTMLResponse)
def kategorije(request: Request, db: Session = Depends(get_db)):
    kategorije = dohvati_sve_kategorije(db)
    return templates.TemplateResponse("kategorije.html", {"request": request, "kategorije": kategorije})

@app.get("/kategorija/{kategorija_id}", response_class=HTMLResponse)
def knjige_po_kategoriji(request: Request, kategorija_id: int, db: Session = Depends(get_db)):
    knjige = get_books_by_kategorija(db, kategorija_id)
    return templates.TemplateResponse("knjige_po_kategoriji.html", {"request": request, "knjige": knjige})

@app.get("/mojracun", response_class=HTMLResponse)
def mojracun(request: Request, db: Session = Depends(get_db)):
    user_id = request.session.get("user_id")
    if not user_id:
        return RedirectResponse("/login")
    korisnik = db.query(Korisnik).filter(Korisnik.id == int(user_id)).first()
    if not korisnik:
        return RedirectResponse("/login")
    return templates.TemplateResponse("mojracun.html", {"request": request, "korisnik": korisnik})

@app.get("/logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/login")
