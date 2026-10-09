import pytest

from app import app


VALID_COURSE = {
    "name": "Intro to Python",
    "description": "Basics of the language",
    "target_date": "2026-12-31",
    "status": "Not Started"
}


@pytest.fixture
def client(tmp_path):
    app.config["TESTING"] = True
    app.config["DATA_FILE"] = str(tmp_path / "courses.json")

    with app.test_client() as client:
        yield client


def create(client, **overrides):
    return client.post("/api/courses", json={**VALID_COURSE, **overrides})


def test_list_is_empty_initially(client):
    response = client.get("/api/courses")

    assert response.status_code == 200
    assert response.get_json() == []


def test_create_course(client):
    response = create(client)
    body = response.get_json()

    assert response.status_code == 201
    assert body["id"] == 1
    assert body["name"] == VALID_COURSE["name"]
    assert "created_at" in body


def test_ids_increment(client):
    create(client)
    response = create(client, name="Second")

    assert response.get_json()["id"] == 2


def test_get_course(client):
    create(client)
    response = client.get("/api/courses/1")

    assert response.status_code == 200
    assert response.get_json()["name"] == VALID_COURSE["name"]


def test_get_missing_course(client):
    response = client.get("/api/courses/99")

    assert response.status_code == 404


@pytest.mark.parametrize("payload, message", [
    ({k: v for k, v in VALID_COURSE.items() if k != "name"}, "Missing fields"),
    ({**VALID_COURSE, "extra": 1}, "Unknown fields"),
    ({**VALID_COURSE, "name": 123}, "name must be a string"),
    ({**VALID_COURSE, "name": "   "}, "name must not be empty"),
    ({**VALID_COURSE, "status": "Done"}, "status must be one of"),
    ({**VALID_COURSE, "target_date": "31/12/2026"}, "YYYY-MM-DD"),
    ({**VALID_COURSE, "target_date": 20261231}, "YYYY-MM-DD"),
])
def test_create_rejects_invalid_data(client, payload, message):
    response = client.post("/api/courses", json=payload)

    assert response.status_code == 400
    assert message in response.get_json()["error"]


def test_create_rejects_non_object_body(client):
    response = client.post("/api/courses", json=["not", "an", "object"])

    assert response.status_code == 400


def test_replace_course_keeps_created_at(client):
    created = create(client).get_json()
    response = client.put(
        "/api/courses/1",
        json={**VALID_COURSE, "status": "In Progress"}
    )
    body = response.get_json()

    assert response.status_code == 200
    assert body["status"] == "In Progress"
    assert body["created_at"] == created["created_at"]


def test_replace_missing_course(client):
    response = client.put("/api/courses/99", json=VALID_COURSE)

    assert response.status_code == 404


def test_patch_course(client):
    create(client)
    response = client.patch("/api/courses/1", json={"status": "Completed"})
    body = response.get_json()

    assert response.status_code == 200
    assert body["status"] == "Completed"
    assert body["name"] == VALID_COURSE["name"]


def test_patch_rejects_invalid_status(client):
    create(client)
    response = client.patch("/api/courses/1", json={"status": "Done"})

    assert response.status_code == 400


def test_delete_course(client):
    create(client)

    assert client.delete("/api/courses/1").status_code == 204
    assert client.get("/api/courses/1").status_code == 404


def test_delete_missing_course(client):
    response = client.delete("/api/courses/99")

    assert response.status_code == 404


def test_data_persists_to_file(client):
    create(client)

    with open(app.config["DATA_FILE"], encoding="utf-8") as file:
        assert '"Intro to Python"' in file.read()
