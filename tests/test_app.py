from http import HTTPStatus

from simple_todo.schemas import UserPublic


def test_read_root(client):
    response = client.get('/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Hello, World!'}


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


def test_read_users(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get('/users')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == [user_schema]


def test_get_user(client, user):
    response = client.get(f'/users/{user.id}')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': user.id,
        'username': user.username,
        'email': user.email,
    }


def test_get_user_not_found(client):
    response = client.get('/users/999')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_update_user(client, user):
    user_data = {
        'username': 'updateduser',
        'email': 'updateduser@example.com',
        'password': 'updatedpassword',
    }

    response = client.put('/users/1', json=user_data)
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': user_data['username'],
        'email': user_data['email'],
        'id': 1,
    }


def test_update_user_not_found(client):
    user_data = {
        'username': 'notUser',
        'email': 'notUser@notUser.com',
        'password': 'updatedpassword',
        'id': 50,
    }

    response = client.put(f'/users/{user_data["id"]}', json=user_data)

    assert response.status_code == HTTPStatus.NOT_FOUND

    assert response.json() == {
        'detail': f'User with id {user_data["id"]} not found'
    }


def test_delete_user(client, user):
    response = client.delete('/users/1')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'message': 'User with id 1 deleted successfully'
    }


def test_delete_user_not_found(client):
    response = client.delete('/users/50')
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User with id 50 not found'}


def test_update_integrity_error(client, user):
    userExample = {
        'username': 'joaozinho',
        'email': 'joaozinho@example.com',
        'password': 'password',
    }

    client.post('/users', json=userExample)

    response = client.put(f'/users/{user.id}', json=userExample)

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Dados já existentes'}
