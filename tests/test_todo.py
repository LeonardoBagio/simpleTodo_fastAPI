from http import HTTPStatus

from simple_todo.models import TodoState


def test_create_todo(client, token):
    response = client.post(
        '/todos/',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'title': 'Test todo',
            'description': 'Test todo description',
            'state': 'draft',
        },
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': 1,
        'title': 'Test todo',
        'description': 'Test todo description',
        'state': 'draft',
    }


def test_create_todo_default_state(client, token):
    response = client.post(
        '/todos/',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'title': 'Test todo',
            'description': 'Test todo description',
        },
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json()['state'] == TodoState.todo.value


def test_create_todo_without_token(client):
    response = client.post(
        '/todos/',
        json={
            'title': 'Test todo',
            'description': 'Test todo description',
            'state': 'draft',
        },
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Not authenticated'}


def test_create_todo_invalid_state(client, token):
    response = client.post(
        '/todos/',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'title': 'Test todo',
            'description': 'Test todo description',
            'state': 'invalid_state',
        },
    )

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
