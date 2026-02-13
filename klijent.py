import datetime
import sqlite3
import socket
import json
import sys

soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def izbor1():
    print("\nPRIJAVA VOLONTERA NA SMENE")
    data={"ime": input("Unesite ime: "),
     "prezime": input("Unesite prezime: "),
     "jmbg": input("Unesite JMBG: "),
     "email": input("Unesite email: "),
     "datum": input("Unesite datum u formatu YYYY-MM-DD: "),
     "smena": input("Izaberite smenu (jutarnja, popodnevna, vecernja): "),
     "pozicija": input("Izaberite poziciju (osoblje za informacije, redar, mediji, posluga u VIP zoni): "),
     "datumPrijave": str(datetime.datetime.now())}
    print(posalji_zahtev("prijava_volontera", data)["poruka"])

def izbor2():
    print("\nREGISTRACIJA KORISNIKA")
    data={"username": input("Unesite username: "),
    "lozinka": input("Unesite lozinku: "),
    "ime": input("Unesite ime: "),
    "prezime": input("Unesite prezime: "),
    "jmbg": input("Unesite JMBG: "),
    "email": input("Unesite email: ")}
    print(posalji_zahtev("registracija", data)["poruka"])

def izbor3():
    username=input("Unesite username: ")
    lozinka=input("Unesite lozinku: ")
    data={
        "username": username,
        "lozinka": lozinka
    }
    poruka = posalji_zahtev("prijavljivanje", data)
    print(poruka)
    if poruka=="Korisnik je uspesno prijavljen.":

        while True:
            print('''Meni:
            1 - Prijava volontera
            2 - Pregled prijava, otkazivanje ili izmena prijave
            0 - Odjavljivanje''')
            match input("Izaberite opciju: "):
                case "0":
                    print("Odjavljivanje uspesno.")
                    return
                case "1": izbor31(username, lozinka)
                case "2": izbor32(username, lozinka)
                case _: return
            input("Klikni ENTER za povratak na meni prijavljenog korisnika.")

def izbor31(username, lozinka):
    data=dict()
    data["username"]=username
    data["datum"]= input("Unesite datum u formatu YYYY-MM-DD: ")
    data["smena"]=input("Izaberite smenu (jutarnja, popodnevna, vecernja): ")
    data["pozicija"]=input("Izaberite poziciju (osoblje za informacije, redar, mediji, posluga u VIP zoni): ")
    data["datumPrijave"] = str(datetime.datetime.now())
    print(posalji_zahtev("prijava_registrovanog_volontera", data)["poruka"])

def izbor32(username, lozinka):
    conn = sqlite3.connect("baza.db")
    c = conn.cursor()
    c.execute("select jmbg, email from registracija where username=?", (username,))
    jmbg, email = c.fetchone()
    data = posalji_zahtev("izlistaj_prijave", (jmbg, email))
    if not data:
        print("Nema prijava za ovog korisnika.")
    else:
        for d in data:
            print(", ".join(f"{k}: {v}" for k, v in d.items()))
        print('''Opcije:
        1 - Izmena prijave
        2 - Otkazivanje prijave
        0 - Povratak na meni''')
        match input("Izaberite opciju: "):
            case "2":
                data2=dict()
                data2["izbor"]=input("Broj prijave: ")
                data2["data"]=data
                print(posalji_zahtev("otkazivanje_prijave", data2))
            case _: return

def izbor4():
    print("\nPREGLED PRIJAVA")
    jmbg=input("Unesite JMBG: ")
    email=input("Unesite email: ")
    data = posalji_zahtev("izlistaj_prijave", (jmbg, email))
    if not data:
        print("Nema prijava za ovog korisnika.")
    else:
        for d in data:
            print(", ".join(f"{k}: {v}" for k, v in d.items()))


def posalji_zahtev(akcija, data):
    zahtev={"akcija": akcija, "data":data}
    soc.send(json.dumps(zahtev).encode())
    return json.loads(soc.recv(2048).decode())

if __name__ == '__main__':
    print("VOLONTIRANJE ZA AUSTRALIAN OPEN 2026")
    try:
        soc.connect(('127.0.0.1', 12345))
        print(soc.recv(1024).decode())
    except socket.error:
        print("Konekcija nije uspela.")
        sys.exit()
    while True:
        print('''Meni:
        1 - Prijava volontera
        2 - Registracija korisnika
        3 - Prijavljivanje korisnika
        4 - Pregled prijava
        0 - Izlazak iz aplikacije''')
        match input("Izaberite opciju: "):
            case "0": sys.exit()
            case "1": izbor1()
            case "2": izbor2()
            case "3": izbor3()
            case "4": izbor4()
            case _: sys.exit()

        input("Klikni ENTER za povratak na meni.")


