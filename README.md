# AO2026 Volunteer Shift Scheduler

A client–server console app for signing up volunteers for shifts at the Australian Open 2026.

**Stack:** Python 3.10+ · TCP sockets · JSON · SQLite · no external dependencies

## Features

| Area | What you can do |
|---|---|
| Sign-up | Pick a date, a shift (morning, afternoon, evening) and a position |
| Accounts | Register once, so personal details are entered only once |
| Status | Each sign-up shows as in progress, locked (within 24 h of the shift) or finished |
| Cancellation | Allowed only while a sign-up is still in progress |

**Rules enforced on the server:** valid 13-digit JMBG and email · date in the future and within the tournament · at most 2 positions per volunteer · caps on evening and afternoon shifts

## Architecture

```
klijent.py (console, JSON over TCP :12345) --> server.py (thread per client)
  --> app.py (rules + validation) --> SQLite
```

## Run

```bash
python server.py    # creates the database on first run
python klijent.py   # run as many clients as you like
```
