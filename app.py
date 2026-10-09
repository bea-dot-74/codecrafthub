from datetime import datetime
import json
import os

from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.config.setdefault("DATA_FILE", "courses.json")

VALID_STATUSES = {
    "Not Started",
    "In Progress",
    "Completed"
}


def read_courses():
    """Read all courses from the JSON file."""
    data_file = app.config["DATA_FILE"]

    if not os.path.exists(data_file):
        return []

    try:
        with open(data_file, "r", encoding="utf-8") as file:
            data = json.load(file)

            if isinstance(data, list):
                return data

            return []

    except json.JSONDecodeError:
        return []


def write_courses(courses):
    """Write all courses to the JSON file."""
    with open(app.config["DATA_FILE"], "w", encoding="utf-8") as file:
        json.dump(courses, file, indent=2)


def find_course(course_id, courses):
    """Find a course by its integer ID."""
    return next(
        (course for course in courses if course["id"] == course_id),
        None
    )


def validate_course_data(data, partial=False):
    """
    Validate incoming course data.

    If partial is True, only supplied fields are validated.
    """
    required_fields = {
        "name",
        "description",
        "target_date",
        "status"
    }

    if not partial:
        missing_fields = required_fields - data.keys()

        if missing_fields:
            return (
                False,
                f"Missing fields: {', '.join(sorted(missing_fields))}"
            )

    allowed_fields = required_fields | {"prerequisites"}

    unknown_fields = set(data.keys()) - allowed_fields

    if unknown_fields:
        return (
            False,
            f"Unknown fields: {', '.join(sorted(unknown_fields))}"
        )

    for field in ("name", "description"):
        if field in data:
            if not isinstance(data[field], str):
                return False, f"{field} must be a string"

            if not data[field].strip():
                return False, f"{field} must not be empty"

    if "status" in data and data["status"] not in VALID_STATUSES:
        return False, (
            "status must be one of: "
            + ", ".join(sorted(VALID_STATUSES))
        )

    if "target_date" in data:
        try:
            datetime.strptime(
                data["target_date"],
                "%Y-%m-%d"
            )
        except (TypeError, ValueError):
            return False, "target_date must use YYYY-MM-DD format"

    if "prerequisites" in data:
        prerequisites = data["prerequisites"]

        if not isinstance(prerequisites, list) or not all(
            isinstance(item, int) and not isinstance(item, bool)
            for item in prerequisites
        ):
            return False, "prerequisites must be a list of course IDs"

        if len(set(prerequisites)) != len(prerequisites):
            return False, "prerequisites must not contain duplicates"

    return True, None


def validate_prerequisites(course_id, prerequisites, courses):
    """
    Check that prerequisites refer to existing courses and
    do not create a cycle (course_id is None for a new course).
    """
    existing_ids = {course["id"] for course in courses}
    missing_ids = [item for item in prerequisites if item not in existing_ids]

    if missing_ids:
        return False, (
            "Prerequisite courses not found: "
            + ", ".join(str(item) for item in missing_ids)
        )

    if course_id is None:
        return True, None

    if course_id in prerequisites:
        return False, "A course cannot be a prerequisite of itself"

    graph = {
        course["id"]: course.get("prerequisites", [])
        for course in courses
    }
    graph[course_id] = prerequisites

    to_visit = list(prerequisites)
    visited = set()

    while to_visit:
        current = to_visit.pop()

        if current == course_id:
            return False, "Prerequisites would create a cycle"

        if current in visited:
            continue

        visited.add(current)
        to_visit.extend(graph.get(current, []))

    return True, None


@app.get("/api/courses")
def get_courses():
    courses = read_courses()
    return jsonify(courses), 200


@app.get("/api/courses/<int:course_id>")
def get_course(course_id):
    courses = read_courses()
    course = find_course(course_id, courses)

    if course is None:
        return jsonify({
            "error": "Course not found"
        }), 404

    return jsonify(course), 200


@app.post("/api/courses")
def create_course():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({
            "error": "Request body must be a JSON object"
        }), 400

    is_valid, error_message = validate_course_data(data)

    if not is_valid:
        return jsonify({
            "error": error_message
        }), 400

    courses = read_courses()
    prerequisites = data.get("prerequisites", [])

    is_valid, error_message = validate_prerequisites(
        None,
        prerequisites,
        courses
    )

    if not is_valid:
        return jsonify({
            "error": error_message
        }), 400

    next_id = max(
        [course["id"] for course in courses],
        default=0
    ) + 1

    new_course = {
        "id": next_id,
        "name": data["name"],
        "description": data["description"],
        "target_date": data["target_date"],
        "status": data["status"],
        "prerequisites": prerequisites,
        "created_at": datetime.now().isoformat(timespec="seconds")
    }

    courses.append(new_course)
    write_courses(courses)

    return jsonify(new_course), 201


@app.put("/api/courses/<int:course_id>")
def replace_course(course_id):
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({
            "error": "Request body must be a JSON object"
        }), 400

    is_valid, error_message = validate_course_data(data)

    if not is_valid:
        return jsonify({
            "error": error_message
        }), 400

    courses = read_courses()
    course = find_course(course_id, courses)

    if course is None:
        return jsonify({
            "error": "Course not found"
        }), 404

    prerequisites = data.get("prerequisites", [])

    is_valid, error_message = validate_prerequisites(
        course_id,
        prerequisites,
        courses
    )

    if not is_valid:
        return jsonify({
            "error": error_message
        }), 400

    course.update({
        "name": data["name"],
        "description": data["description"],
        "target_date": data["target_date"],
        "status": data["status"],
        "prerequisites": prerequisites
    })

    write_courses(courses)

    return jsonify(course), 200


@app.patch("/api/courses/<int:course_id>")
def update_course(course_id):
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({
            "error": "Request body must be a JSON object"
        }), 400

    is_valid, error_message = validate_course_data(
        data,
        partial=True
    )

    if not is_valid:
        return jsonify({
            "error": error_message
        }), 400

    courses = read_courses()
    course = find_course(course_id, courses)

    if course is None:
        return jsonify({
            "error": "Course not found"
        }), 404

    if "prerequisites" in data:
        is_valid, error_message = validate_prerequisites(
            course_id,
            data["prerequisites"],
            courses
        )

        if not is_valid:
            return jsonify({
                "error": error_message
            }), 400

    course.update(data)
    write_courses(courses)

    return jsonify(course), 200


@app.delete("/api/courses/<int:course_id>")
def delete_course(course_id):
    courses = read_courses()
    course = find_course(course_id, courses)

    if course is None:
        return jsonify({
            "error": "Course not found"
        }), 404

    courses.remove(course)

    for other in courses:
        if course_id in other.get("prerequisites", []):
            other["prerequisites"].remove(course_id)

    write_courses(courses)

    return "", 204


if __name__ == "__main__":
    app.run(debug=True)