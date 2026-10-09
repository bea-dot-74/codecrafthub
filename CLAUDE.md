# CodeCraftHub (progetto_test)

Gestore di corsi di apprendimento: API REST Flask + frontend HTML statico.

## Struttura
- `app.py` — API Flask su `/api/courses` (GET, POST, PUT, PATCH, DELETE). I dati sono salvati in `courses.json` (percorso in `app.config["DATA_FILE"]`).
- `index.html` — frontend senza build, chiama `http://localhost:5000/api/courses`.
- `test_app.py` — test pytest dell'API (usano un file dati temporaneo).

## Comandi
- Ambiente virtuale in `.venv` (Python 3.12): `.venv\Scripts\python.exe`
- Installazione: `.venv\Scripts\python.exe -m pip install -r requirements.txt`
- Avvio API: `.venv\Scripts\python.exe app.py` (porta 5000), poi aprire `index.html` nel browser
- Test: `.venv\Scripts\python.exe -m pytest`

## Modello dati di un corso
`id` (int), `name`, `description`, `target_date` (YYYY-MM-DD), `status` ("Not Started" | "In Progress" | "Completed"), `prerequisites` (lista di id, opzionale; niente auto-riferimenti né cicli, validati in `validate_prerequisites`), `created_at` (ISO, impostato dal server).

## Note
- Repository: https://github.com/bea-dot-74/codecrafthub (branch `master`, pubblico).
- Pubblicare su GitHub (commit/push) solo dopo conferma dell'utente.
- Lingua di lavoro con l'utente: italiano.
