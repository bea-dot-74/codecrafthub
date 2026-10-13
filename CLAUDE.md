# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Progetto

CodeCraftHub: gestore di un percorso di studio personale (corsi con data obiettivo, stato e prerequisiti). Due parti senza build:
- `app.py` — API REST Flask su `/api/courses`, unico modulo backend.
- `index.html` — frontend in un solo file (HTML + CSS + JS vanilla), aperto direttamente dal disco; l'indirizzo dell'API è fisso in `API_BASE` (`http://localhost:5000/api/courses`).

## Comandi (Windows, venv in `.venv`, Python 3.12)

```powershell
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe app.py                      # API su porta 5000, debug attivo
.venv\Scripts\python.exe -m pytest                   # tutti i test (35)
.venv\Scripts\python.exe -m pytest test_app.py::test_create_course   # un singolo test
.venv\Scripts\python.exe -m pytest -k prerequisites  # test filtrati per nome
```

Non c'è linter né formatter configurato.

## Architettura backend

- **Persistenza**: nessun database. Ogni richiesta rilegge e riscrive per intero il file JSON indicato da `app.config["DATA_FILE"]` (default `courses.json`, ignorato da git). `read_courses()` restituisce `[]` se il file manca. Se è corrotto o non contiene una lista, ne fa una copia `<file>.corrupt-AAAAMMGG-HHMMSS` (una sola per contenuto) e solleva `CorruptDataFileError`, che diventa un 500 con `{"error": ...}`: il file originale non viene mai sovrascritto e l'API resta bloccata finché non lo si sistema a mano.
- **ID**: `max(id) + 1`, calcolato a ogni POST.
- **Validazione in due fasi**:
  1. `validate_course_data(data, partial)` — forma dei campi (campi obbligatori solo se `partial=False`, campi sconosciuti rifiutati, stato in `VALID_STATUSES`, data `YYYY-MM-DD`, prerequisiti = lista di int senza duplicati; i `bool` sono esclusi esplicitamente).
  2. `validate_prerequisites(course_id, prerequisites, courses)` — controlli sul grafo: id esistenti, niente auto-riferimento, niente cicli (DFS con il grafo aggiornato). `course_id=None` per i nuovi corsi.
- **Semantica dei verbi**: PUT sostituisce tutti i campi modificabili (se `prerequisites` manca diventa `[]`); PATCH aggiorna solo i campi presenti; `id` e `created_at` non sono mai modificabili dal client. DELETE toglie anche l'id dai `prerequisites` degli altri corsi.
- Errori sempre come `{"error": "..."}` con 400/404; DELETE risponde 204 senza corpo.
- Se si aggiunge un campo al corso va aggiornato in più punti: `required_fields`/`allowed_fields` in `validate_course_data`, il dizionario in `create_course`, il `course.update` in `replace_course`, e il frontend.

## Test

`test_app.py` usa il `test_client` di Flask; la fixture `client` punta `DATA_FILE` a un file in `tmp_path`, quindi i test non toccano `courses.json`. L'helper `create(client, **overrides)` crea un corso partendo da `VALID_COURSE`. Il frontend non ha test.

## Documentazione

- `README.md` (inglese) / `README.it.md` (italiano) — funzionalità e API; `INSTALL.md` / `INSTALLAZIONE.md` — guida di installazione. Le coppie di file vanno tenute allineate.

## Note

- Repository: https://github.com/bea-dot-74/codecrafthub (branch `master`, pubblico). Commit e push solo dopo conferma dell'utente.
- Lingua di lavoro con l'utente: italiano.
