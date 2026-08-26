from http import HTTPStatus

import pytest

from simple_todo.models import TodoState
from tests.conftest import TodoFactory


def test_create_todo(client, token):
    response = client.post(
        '/todo/',
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
        '/todo/',
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
        '/todo/',
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
        '/todo/',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'title': 'Test todo',
            'description': 'Test todo description',
            'state': 'invalid_state',
        },
    )

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_list_todos_without_token(client):
    response = client.get('/todo/')

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Not authenticated'}


@pytest.mark.asyncio
async def test_list_todos_empty(client, token):
    response = client.get(
        '/todo/',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'todos': []}


@pytest.mark.asyncio
async def test_list_todos_should_return_all_todos(
    session, client, user, token
):
    expected_todos = 5
    session.add_all(TodoFactory.create_batch(expected_todos, user_id=user.id))
    await session.commit()

    response = client.get(
        '/todo/',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert len(response.json()['todos']) == expected_todos


@pytest.mark.asyncio
async def test_list_todos_only_returns_own_todos(
    session, client, user, other_user, token
):
    session.add_all(TodoFactory.create_batch(3, user_id=user.id))
    session.add_all(TodoFactory.create_batch(2, user_id=other_user.id))
    await session.commit()

    response = client.get(
        '/todo/',
        headers={'Authorization': f'Bearer {token}'},
    )

    expected_todos = 3
    assert response.status_code == HTTPStatus.OK
    assert len(response.json()['todos']) == expected_todos


@pytest.mark.asyncio
async def test_list_todos_pagination(session, client, user, token):
    session.add_all(TodoFactory.create_batch(5, user_id=user.id))
    await session.commit()

    response = client.get(
        '/todo/?offset=1&limit=2',
        headers={'Authorization': f'Bearer {token}'},
    )

    expected_todos = 2
    assert response.status_code == HTTPStatus.OK
    assert len(response.json()['todos']) == expected_todos


@pytest.mark.asyncio
async def test_list_todos_filter_title(session, client, user, token):
    session.add_all(
        TodoFactory.create_batch(3, user_id=user.id, title='Test todo title')
    )
    session.add_all(
        TodoFactory.create_batch(2, user_id=user.id, title='Other subject')
    )
    await session.commit()

    response = client.get(
        '/todo/?title=Test todo title',
        headers={'Authorization': f'Bearer {token}'},
    )

    expected_todos = 3
    assert response.status_code == HTTPStatus.OK
    assert len(response.json()['todos']) == expected_todos


@pytest.mark.asyncio
async def test_list_todos_filter_description(session, client, user, token):
    session.add_all(
        TodoFactory.create_batch(
            3, user_id=user.id, description='important description'
        )
    )
    session.add_all(
        TodoFactory.create_batch(2, user_id=user.id, description='other')
    )
    await session.commit()

    response = client.get(
        '/todo/?description=important',
        headers={'Authorization': f'Bearer {token}'},
    )

    expected_todos = 3
    assert response.status_code == HTTPStatus.OK
    assert len(response.json()['todos']) == expected_todos


@pytest.mark.asyncio
async def test_list_todos_filter_state(session, client, user, token):
    session.add_all(
        TodoFactory.create_batch(3, user_id=user.id, state=TodoState.done)
    )
    session.add_all(
        TodoFactory.create_batch(2, user_id=user.id, state=TodoState.todo)
    )
    await session.commit()

    response = client.get(
        '/todo/?state=done',
        headers={'Authorization': f'Bearer {token}'},
    )

    expected_todos = 3
    assert response.status_code == HTTPStatus.OK
    assert len(response.json()['todos']) == expected_todos


@pytest.mark.asyncio
async def test_list_todos_combined_filters(session, client, user, token):
    session.add_all(
        TodoFactory.create_batch(
            2,
            user_id=user.id,
            title='Combined title',
            description='combined description',
            state=TodoState.doing,
        )
    )
    session.add_all(
        TodoFactory.create_batch(
            3,
            user_id=user.id,
            title='Other title',
            description='other description',
            state=TodoState.todo,
        )
    )
    await session.commit()

    response = client.get(
        '/todo/?title=Combined&description=combined&state=doing',
        headers={'Authorization': f'Bearer {token}'},
    )

    expected_todos = 2
    assert response.status_code == HTTPStatus.OK
    assert len(response.json()['todos']) == expected_todos
