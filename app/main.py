from datetime import date, datetime
from fastapi import FastAPI, Form, Request, Depends, Response, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from starlette.templating import Jinja2Templates
from routers import auth
from database import SessionLocal, engine, Base
from models import Knjiga, Korisnik, ListaZelja, Korpa
from starlette.middleware.sessions import SessionMiddleware
from crud.knjiga import dohvati_sve_kategorije, dohvati_knjige, get_books_by_kategorija
from sqlalchemy.sql.expression import func


# Kreiraj tablice u bazi
Base.metadata.create_all(bind=engine)

app = FastAPI()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
app.add_middleware(SessionMiddleware, secret_key="tajna123")  


# Mountaj static folder za CSS i HTML
app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(auth.router)
templates = Jinja2Templates(directory="templates")



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
async def login_page(request: Request):
    user_id = request.session.get("user_id")
    if user_id:
        return RedirectResponse("/mojracun")
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login")
async def login(
    request: Request, 
    korisnicko_ime: str = Form(...), 
    lozinka: str = Form(...), 
    db: Session = Depends(get_db)
):
    user = db.query(Korisnik).filter(Korisnik.korisnicko_ime == korisnicko_ime).first()
    if not user or not pwd_context.verify(lozinka, user.lozinka):
        return templates.TemplateResponse(
            "login.html", 
            {"request": request, "error": "Neispravno korisničko ime ili lozinka."}
        )
    request.session["user_id"] = user.id
    request.session["korisnik_id"] = user.id
    request.session["korisnicko_ime"] = user.korisnicko_ime
    return RedirectResponse(url="/", status_code=303)

@app.get("/", response_class=HTMLResponse)
def home(request: Request, db: Session = Depends(get_db)):
    korisnik_id = request.session.get("korisnik_id")
    knjige = dohvati_knjige(db)
    bestsellers = db.query(Knjiga).order_by(func.random()).limit(10).all()
    return templates.TemplateResponse("index.html", {"request": request, "bestsellers": bestsellers, "knjige": knjige,
        "korisnik_id": korisnik_id})
                                      

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
    korisnik_id = request.session.get("korisnik_id")
    if not korisnik_id:
        return RedirectResponse("/login")
    korisnik = db.query(Korisnik).filter(Korisnik.id == int(korisnik_id)).first()
    if not korisnik:
        return RedirectResponse("/login")
    return templates.TemplateResponse("mojracun.html", {"request": request, "korisnik": korisnik})

@app.get("/edit-profile", response_class=HTMLResponse)
def edit_profile_get(request: Request, db: Session = Depends(get_db)):
    korisnik_id = request.session.get("korisnik_id")
    if not korisnik_id:
        return RedirectResponse("/login")
    korisnik = db.query(Korisnik).filter(Korisnik.id == int(korisnik_id)).first()
    if not korisnik:
        return RedirectResponse("/login")
    return templates.TemplateResponse("EditProfile.html", {"request": request, "korisnik": korisnik})

@app.post("/edit-profile", response_class=HTMLResponse)
def edit_profile_post(
    request: Request,
    ime: str = Form(...),
    prezime: str = Form(...),
    email: str = Form(...),
    adresa: str = Form(None),
    broj_mobitela: str = Form(None),
    datum_rodenja: str = Form(None),
    db: Session = Depends(get_db)
):
    korisnik_id = request.session.get("korisnik_id")
    if not korisnik_id:
        return RedirectResponse("/login")
    korisnik = db.query(Korisnik).filter(Korisnik.id == int(korisnik_id)).first()
    if not korisnik:
        return RedirectResponse("/login")

    # Provjeri postoji li drugi korisnik s istim emailom
    if db.query(Korisnik).filter(Korisnik.email == email, Korisnik.id != korisnik.id).first():
        return templates.TemplateResponse(
            "EditProfile.html",
            {"request": request, "korisnik": korisnik, "error": "E-mail je već zauzet."}
        )

    korisnik.ime = ime
    korisnik.prezime = prezime
    korisnik.email = email
    korisnik.adresa = adresa
    korisnik.broj_mobitela = broj_mobitela
    if datum_rodenja:
        try:
            korisnik.datum_rodenja = datetime.strptime(datum_rodenja, "%Y-%m-%d").date()
        except ValueError:
            return templates.TemplateResponse(
                "EditProfile.html",
                {"request": request, "korisnik": korisnik, "error": "Neispravan datum rođenja."}
            )
    db.commit()
    db.refresh(korisnik)
    return templates.TemplateResponse(
        "EditProfile.html",
        {"request": request, "korisnik": korisnik, "success": "Profil je uspješno ažuriran!"}
    )

@app.get("/logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/login")

@app.get("/promjenalozinke", response_class=HTMLResponse)
def promjena_lozinke_get(request: Request, db: Session = Depends(get_db)):
    korisnik_id = request.session.get("korisnik_id")
    if not korisnik_id:
        return RedirectResponse("/login")
    return templates.TemplateResponse("promjenalozinke.html", {"request": request})

@app.post("/promjenalozinke", response_class=HTMLResponse)
def promjena_lozinke_post(
    request: Request,
    stara_lozinka: str = Form(...),
    nova_lozinka: str = Form(...),
    potvrda_lozinke: str = Form(...),
    db: Session = Depends(get_db)
):
    korisnik_id = request.session.get("korisnik_id")
    if not korisnik_id:
        return RedirectResponse("/login")
    korisnik = db.query(Korisnik).filter(Korisnik.id == int(korisnik_id)).first()
    if not korisnik:
        return RedirectResponse("/login")

    # Provjeri staru lozinku
    if not pwd_context.verify(stara_lozinka, korisnik.lozinka):
        return templates.TemplateResponse(
            "promjenalozinke.html",
            {"request": request, "error": "Stara lozinka nije točna."}
        )
    # Provjeri podudaranje nove lozinke
    if nova_lozinka != potvrda_lozinke:
        return templates.TemplateResponse(
            "promjenalozinke.html",
            {"request": request, "error": "Nove lozinke se ne podudaraju."}
        )
    if len(nova_lozinka) < 6:
        return templates.TemplateResponse(
            "promjenalozinke.html",
            {"request": request, "error": "Nova lozinka mora imati barem 6 znakova."}
        )

    # Spremi novu lozinku
    korisnik.lozinka = pwd_context.hash(nova_lozinka)
    db.commit()
    return templates.TemplateResponse(
        "promjenalozinke.html",
        {"request": request, "success": "Lozinka je uspješno promijenjena!"}
    )

@app.get("/knjiga/{knjiga_id}", response_class=HTMLResponse)
def detalji_knjige(request: Request, knjiga_id: int, db: Session = Depends(get_db)):
    knjiga = db.query(Knjiga).filter(Knjiga.id == knjiga_id).first()
    if not knjiga:
        return templates.TemplateResponse(
            "404.html", {"request": request, "message": "Knjiga nije pronađena."}, status_code=404
        )
    # Pronađi slične knjige (npr. po kategoriji, osim trenutne)
    slicne_knjige = db.query(Knjiga).filter(
        Knjiga.id != knjiga.id,
        Knjiga.kategorija_id == knjiga.kategorija_id
    ).limit(4).all()
    na_listi_zelja = False
    korisnik_id = request.session.get("korisnik_id")
    if korisnik_id:
        na_listi_zelja = db.query(ListaZelja).filter_by(korisnik_id=korisnik_id, knjiga_id=knjiga_id).first() is not None
    return templates.TemplateResponse(
        "knjiga.html", {"request": request, "knjiga": knjiga, "na_listi_zelja": na_listi_zelja}
    )

@app.get("/zelje", response_class=HTMLResponse)
def wishlist(request: Request, db: Session = Depends(get_db)):
    korisnik_id = request.session.get("korisnik_id")
    if not korisnik_id:
        return RedirectResponse("/login")
    # Dohvati sve knjige na wishlisti korisnika
    lista_zelja_entries = db.query(ListaZelja).filter(ListaZelja.korisnik_id == korisnik_id).all()
    knjige = [entry.knjiga for entry in lista_zelja_entries]
    return templates.TemplateResponse("zelje.html", {"request": request, "knjige": knjige})

@app.post("/zelje/dodaj", response_class=HTMLResponse)
def dodaj_na_wishlist(
    request: Request,
    knjiga_id: int = Form(...),
    db: Session = Depends(get_db)
):
    korisnik_id = request.session.get("korisnik_id")
    if not korisnik_id:
        return RedirectResponse("/login")
    postoji = db.query(ListaZelja).filter_by(korisnik_id=korisnik_id, knjiga_id=knjiga_id).first()
    if not postoji:
        db.add(ListaZelja(korisnik_id=korisnik_id, knjiga_id=knjiga_id))
        db.commit()
    return RedirectResponse(f"/knjiga/{knjiga_id}", status_code=303)

@app.post("/zelje/ukloni", response_class=HTMLResponse)
def ukloni_sa_wishlist(
    request: Request,
    knjiga_id: int = Form(...),
    db: Session = Depends(get_db)
):
    korisnik_id = request.session.get("korisnik_id")
    if not korisnik_id:
        return RedirectResponse("/login")
    entry = db.query(ListaZelja).filter_by(korisnik_id=korisnik_id, knjiga_id=knjiga_id).first()
    if entry:
        db.delete(entry)
        db.commit()
    return RedirectResponse("/zelje", status_code=303)

@app.get("/korpa", response_class=HTMLResponse)
def prikazi_korpu(request: Request, db: Session = Depends(get_db)):
    korisnik_id = request.session.get("korisnik_id")
    if not korisnik_id:
        return RedirectResponse("/login")
    stavke = db.query(Korpa).filter(Korpa.korisnik_id == korisnik_id).all()
    knjige = []
    ukupno = 0.0
    for stavka in stavke:
        if stavka.tip == 2:
            cijena = round(stavka.knjiga.cijena15 or 0, 2)
        elif stavka.tip == 3:
            cijena = round(stavka.knjiga.cijena30 or 0, 2)
        else:  # tip == 1
            cijena = round(stavka.knjiga.cijena or 0, 2)
        ukupno += cijena
        knjige.append({
            "id": stavka.knjiga.id,
            "naslov": stavka.knjiga.naziv_djela,
            "autor": stavka.knjiga.autor,
            "slika_url": stavka.knjiga.slika_url,
            "tip": stavka.tip,
            "cijena": cijena,
            "stavka_id": stavka.id
        })
    return templates.TemplateResponse("korpa.html", {
        "request": request,
        "knjige": knjige,
        "ukupno": ukupno
    })

@app.post("/korpa/dodaj", response_class=HTMLResponse)
def dodaj_u_korpu(
    request: Request,
    knjiga_id: int = Form(...),
    tip: int = Form(...),  # 1 = kupi, 2 = posudi 15, 3 = posudi 30
    db: Session = Depends(get_db)
):
    korisnik_id = request.session.get("korisnik_id")
    if not korisnik_id:
        return RedirectResponse("/login")
    postoji = db.query(Korpa).filter_by(korisnik_id=korisnik_id, knjiga_id=knjiga_id, tip=tip).first()
    if not postoji:
        db.add(Korpa(korisnik_id=korisnik_id, knjiga_id=knjiga_id, tip=tip))
        db.commit()
    return RedirectResponse("/korpa", status_code=303)

@app.post("/korpa/ukloni", response_class=HTMLResponse)
def ukloni_iz_korpe(
    request: Request,
    stavka_id: int = Form(...),
    db: Session = Depends(get_db)
):
    korisnik_id = request.session.get("korisnik_id")
    if not korisnik_id:
        return RedirectResponse("/login")
    stavka = db.query(Korpa).filter_by(id=stavka_id, korisnik_id=korisnik_id).first()
    if stavka:
        db.delete(stavka)
        db.commit()
    return RedirectResponse("/korpa", status_code=303)

@app.post("/korpa/potvrdi")
def potvrdi_narudzbu(request: Request, db: Session = Depends(get_db)):
    korisnik_id = request.session.get("korisnik_id")
    if not korisnik_id:
        return RedirectResponse("/login")
    db.query(Korpa).filter(Korpa.korisnik_id == korisnik_id).delete()
    db.commit()
    return RedirectResponse("/korpa", status_code=303)

def require_admin(request: Request, db: Session):
    korisnik_id = request.session.get("korisnik_id")
    if not korisnik_id:
        return None
    korisnik = db.query(Korisnik).filter_by(id=korisnik_id).first()
    if not korisnik or not korisnik.admin:
        return None
    return korisnik

@app.get("/admin", response_class=HTMLResponse)
def admin_panel(request: Request, db: Session = Depends(get_db)):
    korisnik = require_admin(request, db)
    if not korisnik:
        return RedirectResponse("/", status_code=303)
    korisnici = db.query(Korisnik).all()
    knjige = db.query(Knjiga).all()
    return templates.TemplateResponse("admin.html", {
        "request": request,
        "korisnici": korisnici,
        "knjige": knjige
    })

@app.post("/admin/korisnik/obrisi")
def obrisi_korisnika(
    request: Request,
    korisnik_id: int = Form(...),
    db: Session = Depends(get_db)
):
    korisnik = require_admin(request, db)
    if not korisnik:
        return RedirectResponse("/", status_code=303)
    korisnik_za_brisanje = db.query(Korisnik).filter_by(id=korisnik_id).first()
    if korisnik_za_brisanje:
        db.delete(korisnik_za_brisanje)
        db.commit()
    return RedirectResponse("/admin", status_code=status.HTTP_303_SEE_OTHER)

@app.post("/admin/korisnik/toggle_admin")
def toggle_admin(
    request: Request,
    korisnik_id: int = Form(...),
    db: Session = Depends(get_db)
):
    korisnik = require_admin(request, db)
    if not korisnik:
        return RedirectResponse("/", status_code=303)
    korisnik_za_toggle = db.query(Korisnik).filter_by(id=korisnik_id).first()
    if korisnik_za_toggle:
        korisnik_za_toggle.admin = not korisnik_za_toggle.admin
        db.commit()
    return RedirectResponse("/admin", status_code=status.HTTP_303_SEE_OTHER)

@app.post("/admin/knjiga/dodaj")
def dodaj_knjigu(
    request: Request,
    naslov: str = Form(...),
    autor: str = Form(...),
    cijena: float = Form(...),
    cijena15: float = Form(...),
    cijena30: float = Form(...),
    slika_url: str = Form(...),
    db: Session = Depends(get_db)
):
    korisnik = require_admin(request, db)
    if not korisnik:
        return RedirectResponse("/", status_code=303)
    knjiga = Knjiga(
        naziv_djela=naslov,
        autor=autor,
        cijena=cijena,
        cijena15=cijena15,
        cijena30=cijena30,
        slika_url=slika_url
    )
    db.add(knjiga)
    db.commit()
    return RedirectResponse("/admin", status_code=status.HTTP_303_SEE_OTHER)

@app.post("/admin/knjiga/obrisi")
def obrisi_knjigu(
    request: Request,
    knjiga_id: int = Form(...),
    db: Session = Depends(get_db)
):
    korisnik = require_admin(request, db)
    if not korisnik:
        return RedirectResponse("/", status_code=303)
    knjiga = db.query(Knjiga).filter_by(id=knjiga_id).first()
    if knjiga:
        db.delete(knjiga)
        db.commit()
    return RedirectResponse("/admin", status_code=status.HTTP_303_SEE_OTHER)