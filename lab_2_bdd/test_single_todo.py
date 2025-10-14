import pytest
from pytest_bdd import scenarios, given, when, then, parsers
import json

# Make the Flask app and its in-memory data store accessible to the tests
from lab_2_bdd.app import app, todos

# Constants
EXISTING_TODO = {"id": 2, "task": "Build a Flask API", "done": True}

# Scenarios
scenarios("./features/single_todo.feature")


# Fixtures
@pytest.fixture
def client():
    """Provides a test client for the Flask application."""
    with app.test_client() as client:
        yield client


@pytest.fixture
def response(client):
    """A fixture to store the response from an API call."""
    return {}


@given('the API has a to-do with id 2 and task "Build a Flask API"')
def setup_existing_todo():
    """Set up the initial state with a known to-do item."""
    # Ensure our 'todos' list is in a known state for this test
    global todos
    todos[:] = [
        {"id": 1, "task": "Learn TDD", "done": False},
        EXISTING_TODO,
    ]


@given("the API has a list of to-dos")
def setup_any_todos():
    """Set up the initial state with a generic list."""
    global todos
    todos[:] = [
        {"id": 1, "task": "Learn TDD", "done": False},
        {"id": 2, "task": "Build a Flask API", "done": True},
        {"id": 3, "task": "Example TODO", "done": False},
    ]


@when(parsers.parse("the user requests the to-do with id {todo_id}"))
def get_single_todo(client, response, todo_id):
    """Make a GET request to the /todos/<id> endpoint."""
    res = client.get(f"/todos/{todo_id}")
    response["data"] = res.get_json()
    response["status_code"] = res.status_code


@then(parsers.parse("the response status code should be {status_code:d}"))
def check_status_code(response, status_code):
    """Check if the response status code is the expected one."""
    assert response["status_code"] == status_code


@then("the response should contain the details of the to-do with id 2")
def check_response_for_existing_todo(response):
    """Check the content of the response for a successful request."""
    assert response["data"] == EXISTING_TODO


@then('the response should contain a "not found" error message')
def check_response_for_not_found(response):
    """Check the content of the response for a 404 error."""
    assert "error" in response["data"]
    assert "not found" in response["data"]["error"].lower()


"""Feladat 2: TODO törlés"""


# When lépések a törléshez
@when(parsers.parse("the user deletes the to-do with id {todo_id}"))
def delete_single_todo(client, response, todo_id):
    """Make a DELETE request to the /todos/<id> endpoint."""
    res = client.delete(f"/todos/{todo_id}")
    #response["data"] = res.get_json()
    response["status_code"] = res.status_code


# Then lépések a törlés eredményének ellenőrzéséhez
@then("the response should contain a success message")
def check_response_for_delete_success(response):
    """Check that the response contains a success confirmation."""
    assert "message" in response["data"]
    assert "deleted" in response["data"]["message"].lower()


'''
@then(parsers.parse('no longer exist'))
def check_response_for_

@then('is removed')
def check_todo_is_removed(respone):
    ids_in_list = [item['id'] for item in todos]
    assert todo_id not in ids_in_list

''''''
