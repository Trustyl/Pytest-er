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

    assert client.get('/todos').get_json() == []
    resp = client.post('/todos', json={'title': 'Write tests'})
    assert resp.status_code == 201
    todo = resp.get_json()
    assert todo == {'id': 1, 'title': 'Write tests'}
    assert client.get('/todos').get_json() == [todo]



def test_update_todo(client):
    client.post('/todos', json={'title': 'Old title'})

    resp = client.put('/todos/1', json={'title': 'Updated title'})
    assert resp.status_code == 200
    assert resp.get_json()['title'] == 'Updated title'
    assert client.get('/todos').get_json()[0]['title'] == 'Updated title'



def test_delete_todo(client):
    client.post('/todos', json={'title': 'Disposable'})

    resp = client.delete('/todos/1')
    assert resp.status_code == 204
    assert client.get('/todos').get_json() == []


@pytest.mark.parametrize('payload', [None, {}, {'foo': 'bar'}])
def test_request_validation(client, payload):
    if payload is None:
        resp = client.post('/todos', data='', content_type='application/json')
    else:
        resp = client.post('/todos', json=payload)
    assert resp.status_code == 400
    assert client.get('/todos').get_json() == []
    client.post('/todos', json={'title': 'keep'})
    if payload is None:
        resp = client.put('/todos/1', data='', content_type='application/json')
    else:
        resp = client.put('/todos/1', json=payload)
    assert resp.status_code == 400
    assert client.get('/todos').get_json() == [{'id': 1, 'title': 'keep'}]


def test_nonexistent_ids(client):
    client.post('/todos', json={'title': 'exists'})
    resp = client.put('/todos/999', json={'title': 'x'})
    assert resp.status_code == 404
    resp = client.delete('/todos/999')
    assert resp.status_code == 404
    assert client.get('/todos').get_json() == [{'id': 1, 'title': 'exists'}]


def test_id_increments_after_deletion(client):
    client.post('/todos', json={'title': 'one'})
    client.delete('/todos/1')
    resp = client.post('/todos', json={'title': 'two'})
    assert resp.get_json()['id'] == 2
    assert client.get('/todos').get_json() == [{'id': 2, 'title': 'two'}]


def test_multi_item_interactions(client):
    a = client.post('/todos', json={'title': 'A'}).get_json()
    b = client.post('/todos', json={'title': 'B'}).get_json()
    client.put(f"/todos/{a['id']}", json={'title': 'A1'})
    assert client.get('/todos').get_json() == [{'id': a['id'], 'title': 'A1'}, b]
    client.delete(f"/todos/{b['id']}")
    assert client.get('/todos').get_json() == [{'id': a['id'], 'title': 'A1'}]

