from http import HTTPStatus

from fastapi.testclient import TestClient

from simple_todo.app import app

client = TestClient(app)


def test_read_root():
    response = client.get('/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Hello, World!'}
