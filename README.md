🇬🇧 English | [🇮🇹 Italiano](README.it.md)

# CodeCraftHub

CodeCraftHub helps you plan and track your own learning path. You list the courses you want to take, set a target date for each, and track whether they are not started, in progress or completed. Courses can depend on other courses (prerequisites).

It has two parts:

- **Backend** (`app.py`): a REST API written in Python with Flask. It stores courses in the `courses.json` file.
- **Frontend** (`index.html`): a web page you open in the browser. It talks to the API.

**Quick start (Windows):** see the step-by-step [installation guide](INSTALL.md).

---

## 1. The course

Each course has these fields:

| Field | Description | Required |
|---|---|---|
| `id` | Identifier, assigned automatically | – (automatic) |
| `name` | Course name | Yes |
| `description` | What you will learn | Yes |
| `target_date` | Date by which to complete it, format `YYYY-MM-DD` | Yes |
| `status` | Progress status | Yes |
| `prerequisites` | List of `id`s of courses to take first | No (default: none) |
| `created_at` | Creation date and time, assigned automatically | – (automatic) |

There are three possible statuses:

- **Not Started**
- **In Progress**
- **Completed**

### Prerequisites
A course can have one or more **prerequisites**: other courses to complete first. The link is optional. Rules:

- a course cannot be a prerequisite of itself;
- loops are not allowed (for example, A requires B and B requires A, even through other courses);
- when a course is deleted, it is automatically removed from the prerequisites of the others.

Prerequisites are informational: you can start a course even if its prerequisites are not completed, but the interface flags it.

---

## 2. Web interface features

### Add a course
In the **Add New Course** section, fill in name, target date, description and status, and, if needed, tick the prerequisite courses in the **Prerequisites** box. Then click **Add Course**. The **Clear** button empties the form.
If a field is missing or the date is invalid, an error message appears and the course is not saved.

### View courses
The **Your Courses** section shows a table with all courses:

- name and description;
- prerequisites (**Requires: …**): completed ones have a ✓; if at least one is not completed yet, the row is flagged with ⚠;
- target date;
- status, shown as a colored badge (grey = not started, yellow = in progress, green = completed);
- creation date;
- buttons to edit or delete.

Next to the title, a counter shows the total number of courses. If there are no courses, a message invites you to add one.

### Edit a course
The **Edit** button opens a window with the course data already filled in, prerequisites included (the course itself is not listed). After editing, click **Save Changes**. The window closes with **Cancel**, the **×**, by clicking outside it or by pressing **Esc**.

### Delete a course
The **Remove** button asks for confirmation before deleting the course. This cannot be undone.

### Messages and loading states
- Every operation shows a notification in the top right corner: green on success, red on error.
- While saving, buttons show a loading indicator and cannot be clicked again.
- If the backend does not respond, the page shows the error and a **Retry** button.

### Mobile use
The page adapts to small screens: the form switches to a single column and the table scrolls horizontally.

---

## 3. REST API

Base URL: `http://localhost:5000/api/courses`

| Method | Path | Purpose | Success response |
|---|---|---|---|
| `GET` | `/api/courses` | List all courses | 200 |
| `GET` | `/api/courses/<id>` | Get one course | 200 |
| `POST` | `/api/courses` | Create a course (all fields required) | 201 |
| `PUT` | `/api/courses/<id>` | Replace all data of a course | 200 |
| `PATCH` | `/api/courses/<id>` | Update only some fields | 200 |
| `DELETE` | `/api/courses/<id>` | Delete a course | 204 |

Example request to create a course:

```json
POST /api/courses
{
  "name": "Intro to Python",
  "description": "Language basics",
  "target_date": "2026-12-31",
  "status": "Not Started",
  "prerequisites": [1, 2]
}
```

The `prerequisites` field can be omitted. With `PUT`, send it if you want to keep the prerequisites, otherwise they are cleared; with `PATCH`, it changes only if present.

### Data validation
The API rejects the request with a **400** error and an explanatory message if:

- the request body is not a JSON object;
- a required field is missing (for `POST` and `PUT`);
- an unknown field is present;
- name or description are not text, or are empty;
- the status is not one of the three allowed values;
- the date is not in `YYYY-MM-DD` format;
- prerequisites are not a list of `id`s, contain duplicates or non-existent courses, include the course itself or create a loop.

If the requested course does not exist, the API responds with a **404** error.

---

## 4. Run and test

For step-by-step installation, see [INSTALL.md](INSTALL.md).

```bash
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe app.py
```

With the backend running, open `index.html` in the browser.

To run the automated tests (35 API tests):

```bash
.venv\Scripts\python.exe -m pytest
```
