from flask import Flask, jsonify, request

app = Flask(__name__)

# In-memory data store
todos = [
    {"id": 1, "task": "Learn TDD", "done": False},
    {"id": 2, "task": "Build a Flask API", "done": True},
]


@app.route("/")
def index():
    return "Welcome"


@app.route("/todos", methods=["GET", "POST"])
def get_todos():
    if request.method == "GET":
        return jsonify(todos)
    elif request.method == "POST":
        new_todo = {
            "id": max(todo["id"] for todo in todos) + 1 if todos else 1,
            "task": request.json["task"],
            "done": False,  # New tasks are not done by default
        }
        todos.append(new_todo)
        return jsonify(new_todo), 201


@app.route("/todos/<int:todo_id>", methods=["GET", "DELETE"])
def handle_single_todo(todo_id):
    """
    Handles GET requests for a single to-do item by its ID.
    """
    # Find the todo with the matching ID
    todo = next((item for item in todos if item["id"] == todo_id), None)

    if todo:
        # If found, return the todo item with a 200 OK status
        return jsonify(todo), 200
    else:
        # If not found, return an error message with a 404 Not Found status
        return jsonify({"error": f"Todo with id {todo_id} not found"}), 404

    if request.methot == "GET":
        return jsonify(todo), 200
    if request.methot == "DELETE":
        return "", 204


def _get_next_id():
    """A helper function to get the next ID for a new todo."""
    # If the list is empty, start with ID 1. Otherwise, find the max ID and add 1.
    if not todos:
        return 1
    return max(todo["id"] for todo in todos) + 1
