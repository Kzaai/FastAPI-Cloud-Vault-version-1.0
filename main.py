from fastapi import FastAPI
import os
import json


app = FastAPI()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "sejf.json")


def wczytaj_dane():
    if not os.path.exists(DB_PATH):
        return {}
    with open(DB_PATH, "r", encoding="utf-8") as f:
        return json.load(f)
    
@app.get("/pobierz_wszystko")
def pokaz_sejf():
    dane = wczytaj_dane()
    return{"zawartosc_sejfu": dane}

@app.get("/gdzie_jestem")
def sprawdz_sciezke():
    return {"moja_lokalizacja": DB_PATH}

@app.get("/zapisz/{serwis}/{haslo}")
def zapisz_haslo(serwis: str, haslo: str):
    dane = wczytaj_dane()

    #Wloz haslo
    dane[serwis]= haslo

    #zapisz fizycznie
    with open(DB_PATH, "w", encoding="utf-8") as plik:
        json.dump(dane, plik, indent=4)
    return {"status": "Zapisano !", "dodano_serwis" : serwis}

@app.get("/pobierz/{serwis}")
def daj_haslo(serwis: str):
    dane = wczytaj_dane()
    haslo = dane.get(serwis)

    #Logika jesli nie ma
    if haslo:
        return{"serwis": serwis, "haslo": haslo}
    else:
        return{"blad" : f"Brak hasla dla {serwis}"}
    

@app.get("/usun/{serwis}")
def usun_haslo(serwis: str):
    dane = wczytaj_dane()
    

    #Logika 
    if serwis in dane:
        del dane[serwis] #usuniecie
        with open(DB_PATH, "w", encoding="utf-8") as plik:
            json.dump(dane, plik, indent=4)
        return{"status": "Usunieto", "serwis" : serwis}
    else:
        return{"blad" : f"Brak hasla dla {serwis}"}
    
@app.get("/statystyki")
def statystyki():
    dane = wczytaj_dane()
    return{"liczba_serwisów": len(dane)}