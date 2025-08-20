import os
import sys
import pytest

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from app import create_app


@pytest.fixture
def client():
    app = create_app()
    app.config.update({'TESTING': True})
    with app.test_client() as client:
        yield client


def test_create_and_list_todo(client):
    resp = client.get('/todos')
    assert resp.status_code == 200
    assert resp.get_json() == []

    resp = client.post('/todos', json={'title': 'Write tests'})
    assert resp.status_code == 201
    todo = resp.get_json()
    assert todo['id'] == 1
    assert todo['title'] == 'Write tests'

    resp = client.get('/todos')
    assert resp.status_code == 200
    assert resp.get_json() == [todo]


def test_update_todo(client):
    client.post('/todos', json={'title': 'Old title'})

    resp = client.put('/todos/1', json={'title': 'Updated title'})
    assert resp.status_code == 200
    updated = resp.get_json()
    assert updated['title'] == 'Updated title'

    resp = client.get('/todos')
    assert resp.get_json()[0]['title'] == 'Updated title'


def test_delete_todo(client):
    client.post('/todos', json={'title': 'Disposable'})

    resp = client.delete('/todos/1')
    assert resp.status_code == 204

    resp = client.get('/todos')
    assert resp.status_code == 200
    assert resp.get_json() == []
