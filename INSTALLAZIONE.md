[🇬🇧 English](INSTALL.md) | 🇮🇹 Italiano

# CodeCraftHub – Manuale d'installazione (Windows)

Questa guida porta da zero a CodeCraftHub funzionante sul proprio computer. Per cosa fa l'applicazione, vedi il [README](README.it.md).

> **I comandi di questa guida sono solo per Windows.** Su macOS e Linux i passi sono gli stessi, ma i comandi cambiano.

Tutti i comandi vanno scritti nel terminale **PowerShell**.

---

## 1. Cosa serve prima

- **Python 3.12.** Si scarica da <https://www.python.org/downloads/>. Durante l'installazione spuntare **«Add python.exe to PATH»**.
- **Git**, per scaricare il progetto: <https://git-scm.com/download/win>.
- **Un browser** qualsiasi.

Per controllare che siano installati:

```powershell
py -3.12 --version
git --version
```

Ognuno dei due comandi deve stampare un numero di versione.

---

## 2. Scaricare il progetto

Scegliere la cartella in cui mettere il progetto, poi:

```powershell
git clone https://github.com/bea-dot-74/codecrafthub.git
cd codecrafthub
```

**Da qui in avanti, tutti i comandi si danno dentro la cartella `codecrafthub`.**

---

## 3. Creare l'ambiente virtuale

L'ambiente virtuale è una cartella (`.venv`) che contiene un Python e delle librerie riservati a questo progetto. Così le librerie installate qui non si mescolano con quelle di altri progetti.

```powershell
py -3.12 -m venv .venv
```

Si fa una volta sola. Alla fine compare la cartella `.venv`.

---

## 4. Installare le librerie

```powershell
.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Il file `requirements.txt` elenca le librerie necessarie, con la versione esatta:

| Libreria | A cosa serve |
|---|---|
| Flask | il server web che risponde alle richieste |
| Werkzeug | componente su cui si appoggia Flask |
| Flask-Cors | permette alla pagina `index.html` di parlare con l'API |
| pytest | esegue i test automatici |

---

## 5. Avviare l'API

```powershell
.venv\Scripts\python.exe app.py
```

L'API parte sulla porta **5000** e il terminale resta occupato finché è accesa. Per spegnerla: **Ctrl+C**.

**Verifica:** aprire nel browser <http://localhost:5000/api/courses>.
Se non ci sono ancora corsi, compare `[]` (una lista vuota). Se compare un errore di connessione, l'API non è partita: rileggere il messaggio nel terminale.

---

## 6. Aprire l'interfaccia

Con l'API accesa, fare doppio clic su `index.html` (oppure trascinarlo nel browser).
La pagina mostra il modulo **Add New Course** e la tabella **Your Courses**.

---

## 7. Lanciare i test

In un **secondo** terminale (il primo è occupato dall'API), sempre nella cartella del progetto:

```powershell
.venv\Scripts\python.exe -m pytest
```

Alla fine deve comparire `35 passed`. I test usano un file dati temporaneo: non toccano i corsi salvati.

---

## 8. Dove finiscono i dati

I corsi sono salvati nel file `courses.json`, creato al primo salvataggio **nella cartella da cui si è avviata l'API**. Per questo l'API va sempre avviata dalla cartella del progetto: da un'altra cartella si troverebbe un elenco vuoto.

> ⚠️ **Prima di modificare `courses.json` a mano, farne una copia.**
> Se il file contiene un errore di formato, l'API ne salva una copia accanto (`courses.json.corrupt-` seguito da data e ora) e risponde a ogni richiesta con un errore finché il file non viene corretto o rimosso. Il file originale non viene mai sovrascritto.

---

## 9. Problemi comuni

| Sintomo | Causa probabile | Cosa fare |
|---|---|---|
| `py` o `python` «non è riconosciuto» | Python non è installato o non è nel PATH | Reinstallare Python spuntando «Add python.exe to PATH», poi aprire un nuovo terminale |
| `.venv\Scripts\python.exe` non trovato | Ambiente virtuale non creato, oppure terminale nella cartella sbagliata | Controllare di essere in `codecrafthub`, poi ripetere il passo 3 |
| `ModuleNotFoundError: No module named 'flask'` | Librerie non installate | Ripetere il passo 4 |
| All'avvio: «Address already in use» o simile | La porta 5000 è occupata da un altro programma (o da un'altra copia dell'API) | Chiudere l'altro terminale con l'API; per vedere chi usa la porta: `netstat -ano \| findstr :5000` |
| La pagina mostra un errore e il pulsante **Retry** | L'API è spenta | Avviarla (passo 5), poi cliccare **Retry** |
| L'elenco dei corsi è vuoto, ma prima non lo era | API avviata da un'altra cartella | Spegnerla e riavviarla dalla cartella del progetto |
