🇬🇧 English | [🇮🇹 Italiano](INSTALLAZIONE.md)

# CodeCraftHub – Installation guide (Windows)

This guide takes you from zero to a working CodeCraftHub on your computer. For what the application does, see the [README](README.md).

> **The commands in this guide are for Windows only.** On macOS and Linux the steps are the same, but the commands differ.

Type all commands in a **PowerShell** terminal.

---

## 1. What you need first

- **Python 3.12.** Download it from <https://www.python.org/downloads/>. During installation, tick **"Add python.exe to PATH"**.
- **Git**, to download the project: <https://git-scm.com/download/win>.
- **Any browser.**

To check they are installed:

```powershell
py -3.12 --version
git --version
```

Each command must print a version number.

---

## 2. Download the project

Choose the folder where you want the project, then:

```powershell
git clone https://github.com/bea-dot-74/codecrafthub.git
cd codecrafthub
```

**From here on, run every command inside the `codecrafthub` folder.**

---

## 3. Create the virtual environment

A virtual environment is a folder (`.venv`) holding a Python and libraries reserved for this project, so they do not mix with those of other projects.

```powershell
py -3.12 -m venv .venv
```

You only do this once. When it finishes, the `.venv` folder appears.

---

## 4. Install the libraries

```powershell
.venv\Scripts\python.exe -m pip install -r requirements.txt
```

`requirements.txt` lists the required libraries, with exact versions:

| Library | What it is for |
|---|---|
| Flask | the web server that answers requests |
| Werkzeug | component Flask is built on |
| Flask-Cors | lets the `index.html` page talk to the API |
| pytest | runs the automated tests |

---

## 5. Start the API

```powershell
.venv\Scripts\python.exe app.py
```

The API starts on port **5000** and keeps the terminal busy while it runs. To stop it: **Ctrl+C**.

**Check:** open <http://localhost:5000/api/courses> in the browser.
If there are no courses yet, you see `[]` (an empty list). If you get a connection error, the API did not start: read the message in the terminal.

---

## 6. Open the interface

With the API running, double-click `index.html` (or drag it into the browser).
The page shows the **Add New Course** form and the **Your Courses** table.

---

## 7. Run the tests

In a **second** terminal (the first one is busy with the API), still in the project folder:

```powershell
.venv\Scripts\python.exe -m pytest
```

At the end you should see `35 passed`. The tests use a temporary data file: they do not touch your saved courses.

---

## 8. Where the data goes

Courses are saved in `courses.json`, created on the first save **in the folder the API was started from**. That is why you must always start the API from the project folder: from another folder you would see an empty list.

> ⚠️ **Make a copy of `courses.json` before editing it by hand.**
> If the file has a format error, the API saves a copy next to it (`courses.json.corrupt-` followed by date and time) and answers every request with an error until the file is fixed or removed. The original file is never overwritten.

---

## 9. Common problems

| Symptom | Likely cause | What to do |
|---|---|---|
| `py` or `python` "is not recognized" | Python is not installed or not in PATH | Reinstall Python ticking "Add python.exe to PATH", then open a new terminal |
| `.venv\Scripts\python.exe` not found | Virtual environment not created, or terminal in the wrong folder | Make sure you are in `codecrafthub`, then repeat step 3 |
| `ModuleNotFoundError: No module named 'flask'` | Libraries not installed | Repeat step 4 |
| On start: "Address already in use" or similar | Port 5000 is used by another program (or another copy of the API) | Close the other terminal running the API; to see what uses the port: `netstat -ano \| findstr :5000` |
| The page shows an error and a **Retry** button | The API is not running | Start it (step 5), then click **Retry** |
| The course list is empty, but it was not before | API started from another folder | Stop it and restart it from the project folder |
