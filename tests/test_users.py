from http import HTTPStatus

from simple_todo.schemas import UserPublic
from tests.conftest import UserFactory


def test_create_user(client):
    user_data = UserFactory.build()

    response = client.post(
        '/users',
        json={
            'username': user_data.username,
            'email': user_data.email,
            'password': user_data.password,
        },
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'username': user_data.username,
        'email': user_data.email,
        'id': 1,
    }


def test_read_users(client, user, token):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get(
        '/users', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == [user_schema]


def test_get_user(client, user, token):
    response = client.get(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': user.id,
        'username': user.username,
        'email': user.email,
    }


def test_update_user(client, user, token):
    user_data = UserFactory.build()

    response = client.put(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': user_data.username,
            'email': user_data.email,
            'password': user_data.password,
        },
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': user_data.username,
        'email': user_data.email,
        'id': user.id,
    }


def test_update_integrity_error(client, user, other_user, token):
    response = client.put(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': other_user.username,
            'email': other_user.email,
            'password': other_user.password,
        },
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Dados já existentes'}


def test_delete_user(client, user, token):
    response = client.delete(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'message': f'User with id {user.id} deleted successfully'
    }


def test_create_user_conflict(client, user):
    other = UserFactory.build()
    response = client.post(
        '/users',
        json={
            'username': user.username,
            'email': other.email,
            'password': other.password,
        },
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Dados já existentes'}


def test_get_user_forbidden(client, user, token):
    response = client.get(
        f'/users/{user.id + 1}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {'detail': 'Not enough permissions'}


def test_update_user_forbidden(client, user, token):
    user_data = UserFactory.build()
    response = client.put(
        f'/users/{user.id + 1}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': user_data.username,
            'email': user_data.email,
            'password': user_data.password,
        },
    )

    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {'detail': 'Not enough permissions'}


def test_delete_user_forbidden(client, user, token):
    response = client.delete(
        f'/users/{user.id + 1}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {'detail': 'Not enough permissions'}


def test_update_user_with_wrong_user(client, other_user, token):
    user_data = UserFactory.build()
    response = client.put(
        f'/users/{other_user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': user_data.username,
            'email': user_data.email,
            'password': user_data.password,
        },
    )

    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {'detail': 'Not enough permissions'}
