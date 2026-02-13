import socket
import threading
import json
from app import inicijalizacija_baze, izlistaj_prijave, registracija, prijava_volontera, prijavljivanje, \
    prijava_registrovanog_volontera, otkazivanje_prijave


def obradi_zahtev(c):
    while True:
        zahtev = json.loads(c.recv(2048).decode())
        akcija = zahtev["akcija"]
        data = zahtev["data"]
        if akcija=="prijava_volontera": c.send(json.dumps(prijava_volontera(data)).encode())
        elif akcija=="izlistaj_prijave": c.send(json.dumps(izlistaj_prijave(data)).encode())
        elif akcija=="registracija": c.send(json.dumps(registracija(data)).encode())
        elif akcija=="prijavljivanje": c.send(json.dumps(prijavljivanje(data)).encode())
        elif akcija=="prijava_registrovanog_volontera": c.send(json.dumps(prijava_registrovanog_volontera(data)).encode())
        elif akcija=="izmena_prijave": c.send(json.dumps(izmena_prijave(data)).encode())
        elif akcija=="otkazivanje_prijave": c.send(json.dumps(otkazivanje_prijave(data)).encode())


if __name__ == '__main__':
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    soc.bind(('', 12345))
    soc.listen(5)
    inicijalizacija_baze()
    while True:
        c, addr=soc.accept()
        c.send(f"Uspesno povezivanje! Adresa: {addr[0]}".encode())
        threading.Thread(target=obradi_zahtev, args=(c,)).start()
