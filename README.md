# CodeCraftHub – Funzionalità

CodeCraftHub è una piattaforma per pianificare e seguire il proprio percorso di apprendimento. Permette di registrare i corsi che si vogliono seguire, fissare una data obiettivo e tenere traccia dello stato di avanzamento.

L'applicazione è composta da due parti:

- **Backend** (`app.py`): un'API REST scritta in Python con Flask, che salva i corsi nel file `courses.json`.
- **Frontend** (`index.html`): una pagina web che si apre nel browser e comunica con l'API.

---

## 1. Il corso

Ogni corso ha queste informazioni:

| Campo | Descrizione | Obbligatorio |
|---|---|---|
| `id` | Numero identificativo, assegnato automaticamente | – (automatico) |
| `name` | Nome del corso | Sì |
| `description` | Cosa si imparerà | Sì |
| `target_date` | Data entro cui completarlo, formato `AAAA-MM-GG` | Sì |
| `status` | Stato di avanzamento | Sì |
| `created_at` | Data e ora di creazione, assegnata automaticamente | – (automatico) |

Gli stati possibili sono tre:

- **Not Started** – non ancora iniziato
- **In Progress** – in corso
- **Completed** – completato

---

## 2. Funzionalità dell'interfaccia web

### Aggiungere un corso
Nella sezione **Add New Course** si compilano nome, data obiettivo, descrizione e stato, poi si clicca **Add Course**. Il pulsante **Clear** svuota il modulo.
Se manca un campo o la data non è valida, compare un messaggio di errore e il corso non viene salvato.

### Visualizzare i corsi
La sezione **Your Courses** mostra una tabella con tutti i corsi:

- nome e descrizione;
- data obiettivo;
- stato, evidenziato con un'etichetta colorata (grigio = non iniziato, giallo = in corso, verde = completato);
- data di creazione;
- pulsanti per modificare o eliminare.

Accanto al titolo c'è un contatore con il numero totale dei corsi. Se non ci sono corsi, compare un invito ad aggiungerne uno.

### Modificare un corso
Il pulsante **Edit** apre una finestra con i dati del corso già compilati. Dopo le modifiche si clicca **Save Changes**. La finestra si chiude con **Cancel**, con la **×**, cliccando fuori o premendo **Esc**.

### Eliminare un corso
Il pulsante **Remove** chiede conferma prima di cancellare il corso. L'operazione non si può annullare.

### Messaggi e stati di caricamento
- Ogni operazione mostra una notifica in alto a destra: verde se è riuscita, rossa in caso di errore.
- Durante il salvataggio i pulsanti mostrano un indicatore di caricamento e non si possono cliccare di nuovo.
- Se il backend non risponde, la pagina mostra l'errore e un pulsante **Retry** per riprovare.

### Uso da smartphone
La pagina si adatta agli schermi piccoli: il modulo passa su una colonna e la tabella si può scorrere in orizzontale.

---

## 3. API REST

Indirizzo base: `http://localhost:5000/api/courses`

| Metodo | Percorso | Funzione | Risposta se riesce |
|---|---|---|---|
| `GET` | `/api/courses` | Elenco di tutti i corsi | 200 |
| `GET` | `/api/courses/<id>` | Dettaglio di un corso | 200 |
| `POST` | `/api/courses` | Crea un nuovo corso (tutti i campi obbligatori) | 201 |
| `PUT` | `/api/courses/<id>` | Sostituisce tutti i dati di un corso | 200 |
| `PATCH` | `/api/courses/<id>` | Modifica solo alcuni campi | 200 |
| `DELETE` | `/api/courses/<id>` | Elimina un corso | 204 |

Esempio di richiesta per creare un corso:

```json
POST /api/courses
{
  "name": "Intro to Python",
  "description": "Basi del linguaggio",
  "target_date": "2026-12-31",
  "status": "Not Started"
}
```

### Controlli sui dati
L'API rifiuta la richiesta con errore **400** e un messaggio esplicativo se:

- il corpo della richiesta non è un oggetto JSON;
- manca un campo obbligatorio (per `POST` e `PUT`);
- è presente un campo non previsto;
- nome o descrizione non sono testo, oppure sono vuoti;
- lo stato non è uno dei tre ammessi;
- la data non è nel formato `AAAA-MM-GG`.

Se il corso richiesto non esiste, l'API risponde con errore **404**.

---

## 4. Avvio e test

```bash
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe app.py
```

Con il backend avviato, aprire `index.html` nel browser.

Per eseguire i test automatici (20 test sull'API):

```bash
.venv\Scripts\python.exe -m pytest
```
