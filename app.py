import datetime
import sqlite3
def inicijalizacija_baze():
    conn = sqlite3.connect("baza.db")
    c = conn.cursor()
    c.execute('''create table if not exists prijava(
        id integer primary key autoincrement,
        ime varchar,
        prezime varchar,
        jmbg varchar,
        email varchar,
        datum date,
        smena varchar,
        pozicija varchar,
        datumPrijave date)'''
              )
    c.execute('''create table if not exists registracija(
        id integer primary key autoincrement,
        username varchar,
        lozinka varchar,
        ime varchar,
        prezime varchar,
        jmbg varchar,
        email varchar
    )''')
    conn.commit()
    conn.close()

def data_check(data, izbor):
    if len(data["jmbg"])!=13: return "notok", "JMBG mora da ima 13 cifara"
    if not data["jmbg"].isdigit(): return "notok", "JMBG mora da se sastoji od cifara"
    if '@' not in data["email"]: return "notok", "Email adresa nije validna"
    if izbor=="registracija": return "ok", ""
    try:
        d = datetime.datetime.strptime(data["datum"], "%Y-%m-%d")
    except ValueError:
        return "notok", "Datum nije validan"
    d = datetime.datetime.strptime(data["datum"], "%Y-%m-%d")
    if(d.date()<=datetime.date.today()): return "notok", "Datum mora biti od sutra nadalje"
    if(d>datetime.datetime(2026, 2, 5)): return "notok", "Datum je nakon kraja turnira"
    if data["smena"].lower() not in ["jutarnja", "popodnevna", "vecernja"]: return "notok", "Smena nije validna"
    if data["pozicija"].lower() not in ["osoblje za informacije", "redar", "mediji", "posluga u vip zoni"]: return "notok", "Pozicija nije validna"
    conn=sqlite3.connect("baza.db")
    cur=conn.cursor()
    cur.execute("select pozicija from prijava where jmbg=?", (data["jmbg"],))
    s = set(ss[0] for ss in cur.fetchall())
    if (len(s)==2 and data["pozicija"] not in s) or len(s)>2: return "notok", "Korisnik se prijavio na preko 2 razlicite pozicije"
    cur.execute("select * from prijava where jmbg=? and smena=?", (data["jmbg"], "vecernja",))
    if len(cur.fetchall())>3: return "notok", "Maksimalan broj vecernjih termina je 3"
    cur.execute("select * from prijava where jmbg=? and smena=?", (data["jmbg"], "popodnevna",))
    if len(cur.fetchall()) > 5: return "notok", "Maksimalan broj popodnevnih termina je 5"
    conn.close()
    return "ok", ""

def prijava_volontera(data):
    konekcija, poruka = data_check(data, "prijava")
    if konekcija=="notok": return {"konekcija": konekcija, "poruka": poruka}
    conn = sqlite3.connect("baza.db")
    c=conn.cursor()
    kolone = ", ".join(data.keys())
    vrednosti = list(data.values())
    upitnici = ', '.join(["?"]*len(data))
    c.execute(f"INSERT INTO prijava ({kolone}) VALUES ({upitnici})", vrednosti)
    conn.commit()
    conn.close()
    with open(f'{data["ime"]}_{data["prezime"]}_{data["datum"]}_prijava.txt', "a") as fobj:
        for (k, v) in data.items():
            fobj.write(f"{k}: {v}\n")
    return {"konekcija": "ok", "poruka": "Korisnik je uspesno prijavljen."}

def prijava_registrovanog_volontera(data):
    conn = sqlite3.connect("baza.db")
    c = conn.cursor()
    c.execute("select ime, prezime, jmbg, email from registracija where username=?", (data["username"],))
    kolone = [d[0] for d in c.description]
    vrednosti = list(c.fetchone())
    data2 = dict(zip(kolone, vrednosti))
    for k, v in data.items():
        if(k!='username'): data2[k]=v
    return prijava_volontera(data2)

def izlistaj_prijave(data):
    conn=sqlite3.connect("baza.db")
    c=conn.cursor()
    jmbg, email = data
    c.execute("select * from prijava where jmbg=? and email=?", (jmbg, email,))
    kolone = [d[0] for d in c.description]
    ans = [dict(zip(kolone, vrednost)) for vrednost in c.fetchall()]
    sad=datetime.datetime.now()
    for i in range(len(ans)):
        d = datetime.datetime.strptime(ans[i]["datum"], "%Y-%m-%d")
        ans[i]["status"]="zavrsena"
        if sad<d<sad+datetime.timedelta(days=1): ans[i]["status"]="zakljucana"
        elif d>sad+datetime.timedelta(days=1): ans[i]["status"]="u obradi"
    conn.close()
    return ans




def registracija(data):
    konekcija, poruka = data_check(data, "registracija")
    if konekcija=="notok": return {"konekcija": konekcija, "poruka": poruka}
    conn=sqlite3.connect("baza.db")
    c=conn.cursor()
    c.execute("select * from registracija where username=?", (data["username"],))
    if c.fetchone() is not None:
        conn.close()
        return "Korisnik vec postoji."
    kolone = ", ".join(data.keys())
    vrednosti=list(data.values())
    upitnici=", ".join(["?"]*len(data))
    c.execute(f"insert into registracija ({kolone}) values ({upitnici})", vrednosti)
    conn.commit()
    conn.close()
    return {"konekcija": "ok", "poruka": "Registracija uspesna."}

def prijavljivanje(data):
    username =data["username"]
    lozinka = data["lozinka"]
    conn=sqlite3.connect("baza.db")
    c=conn.cursor()
    c.execute("select * from registracija where username=?", (username,))
    if c.fetchone() is None:
        conn.close()
        return "Korisnik nije registrovan."
    else:
        conn.close()
        return "Korisnik je uspesno prijavljen."

def otkazivanje_prijave(data2):
    izbor=data2["izbor"]
    data=data2["data"]
    if izbor not in [str(d["id"]) for d in data]:
        return "Prijava ne postoji."
    izbor=int(izbor)
    for d in data:
        if d["id"]==izbor and d["status"]!="u obradi":
            return "Prijava je zakljucana ili zavrsena."
    conn=sqlite3.connect("baza.db")
    c=conn.cursor()
    c.execute("delete from prijava where id=?", (izbor,))
    conn.commit()
    conn.close()
    return f"Prijava {izbor} je otkazana."
