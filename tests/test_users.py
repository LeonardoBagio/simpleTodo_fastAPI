from http import HTTPStatus

from simple_todo.schemas import UserPublic


def test_create_user(client):
    user_data = {
        'username': 'testuser',
        'email': 'testuser@example.com',
        'password': 'testpassword',
    }

    response = client.post('/users', json=user_data)
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'username': user_data['username'],
        'email': user_data['email'],
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
    user_data = {
        'username': 'updateduser',
        'email': 'updateduser@example.com',
        'password': 'updatedpassword',
    }

    response = client.put(
        '/users/1',
        headers={'Authorization': f'Bearer {token}'},
        json=user_data,
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': user_data['username'],
        'email': user_data['email'],
        'id': 1,
    }


def test_update_integrity_error(client, user, token):
    userExample = {
        'username': 'joaozinho',
        'email': 'joaozinho@example.com',
        'password': 'password',
    }

    client.post('/users', json=userExample)

    response = client.put(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json=userExample,
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
