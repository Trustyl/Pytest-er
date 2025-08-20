# Regression Testing for Flask Todo API

This document describes the design of the sample Flask Todo API and the
regression tests built with `pytest` to protect its behavior.

## Application Overview

The API is created via a small factory function `create_app` located in
`app.py`. It stores todos in an in-memory list and assigns identifiers using
an incrementing counter. The counter and list live in the closure of the
factory, giving each app instance isolated state and making tests
independent.

Key routes:

- `GET /todos` – returns the current list as JSON.
- `POST /todos` – accepts a JSON payload with a `title` and creates a new
todo. A `201` status code signals successful creation.
- `PUT /todos/<id>` – updates an existing todo's title.
- `DELETE /todos/<id>` – removes a todo, responding with `204` when
successful.

## Test Strategy

Regression tests ensure each route continues to work across code changes.
A pytest fixture named `client` constructs a fresh application and yields a
Flask `test_client`. This mock client lets us perform HTTP calls without
running a server. Because `create_app` returns a new closure every time,
state does not leak between tests.

### Test Cases

1. **Creation and Listing**
   - Assert the initial list is empty.
   - POST a todo and expect a structured JSON response with `id` and `title`.
   - Retrieve the list and confirm the new item appears.
2. **Updating**
   - Create a todo then change its title via `PUT`.
   - Verify both the response and subsequent `GET` reflect the update.
3. **Deletion**
   - Create a todo and delete it.
   - Confirm the API returns `204` and the list is empty again.
4. **Request Validation**
   - Parameterized over `None`, an empty dict, and a dict missing `title` to
     ensure malformed payloads return `400` and leave state unchanged.
5. **Non‑existent IDs**
   - Updating or deleting `999` yields `404` and does not disturb existing
     todos.
6. **ID Incrementation**
   - Create a todo, delete it, then create another and check the new todo
     receives the next sequential identifier.
7. **Multi‑item Interactions**
   - Create two todos, update the first, and delete the second. The remaining
     todo should retain its updated title, demonstrating operations are
     isolated.

## Why These Constructs?

- **Factory Pattern** – Using a factory with a closure-scoped list and
  `nonlocal` counter provides simple state management while keeping tests
  isolated.
- **pytest Fixtures** – Fixtures offer concise setup/teardown and make the
  test code easy to read.
- **Flask `test_client`** – Simulates HTTP requests quickly, avoiding the
  overhead of running a real server.
- **Parameterized Tests** – `pytest.mark.parametrize` exercises multiple
  malformed payloads with a single test function, increasing coverage while
  minimizing duplication.

## Running the Tests

```bash
pip install -r requirements.txt
pytest
```
