from http import HTTPStatus

import pytest
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from simple_todo.models import Category, Status, Todo
from tests.conftest import TodoFactory


async def _status_id(session, code):
    return await session.scalar(select(Status.id).where(Status.code == code))


async def _category_id(session, code):
    return await session.scalar(
        select(Category.id).where(Category.code == code)
    )


def test_create_todo(client, token, status, category):
    response = client.post(
        '/todo/',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'title': 'Test todo',
            'description': 'Test todo description',
            'status_id': status.id,
            'category_id': category.id,
            'issue': 'GH-123',
        },
    )

    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert data['id'] == 1
    assert data['title'] == 'Test todo'
    assert data['description'] == 'Test todo description'
    assert data['status_id'] == status.id
    assert data['category_id'] == category.id
    assert data['issue'] == 'GH-123'
    assert 'created_at' in data
    assert 'updated_at' in data


def test_create_todo_default_status(client, token, status):
    response = client.post(
        '/todo/',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'title': 'Test todo',
            'description': 'Test todo description',
        },
    )

    assert response.status_code == HTTPStatus.OK
    data = response.json()
    # Sem status_id → cai no default 'nao_iniciada'.
    assert data['status_id'] == status.id
    assert data['category_id'] is None
    assert data['issue'] is None


def test_create_todo_without_token(client):
    response = client.post(
        '/todo/',
        json={
            'title': 'Test todo',
            'description': 'Test todo description',
        },
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Not authenticated'}


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
async def test_list_todos_should_return_all_fields(
    session, client, user, token, mock_db_time
):
    status_id = await _status_id(session, 'nao_iniciada')
    category_id = await _category_id(session, 'feature')
    with mock_db_time(model=Todo) as time:
        todo = TodoFactory.create(
            user_id=user.id,
            title='Full field todo',
            description='Full field description',
            status_id=status_id,
            category_id=category_id,
            issue='JIRA-9',
        )
        session.add(todo)
        await session.commit()
        await session.refresh(todo)

    response = client.get(
        '/todo/',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json()['todos'] == [
        {
            'id': todo.id,
            'title': 'Full field todo',
            'description': 'Full field description',
            'status_id': status_id,
            'category_id': category_id,
            'issue': 'JIRA-9',
            'created_at': time.isoformat(),
            'updated_at': time.isoformat(),
        }
    ]


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
async def test_list_todos_filter_status(session, client, user, token):
    done_id = await _status_id(session, 'concluido')
    todo_id = await _status_id(session, 'nao_iniciada')
    session.add_all(
        TodoFactory.create_batch(3, user_id=user.id, status_id=done_id)
    )
    session.add_all(
        TodoFactory.create_batch(2, user_id=user.id, status_id=todo_id)
    )
    await session.commit()

    response = client.get(
        f'/todo/?status_id={done_id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    expected_todos = 3
    assert response.status_code == HTTPStatus.OK
    assert len(response.json()['todos']) == expected_todos


@pytest.mark.asyncio
async def test_list_todos_filter_category(
    session, client, user, token, category
):
    session.add_all(
        TodoFactory.create_batch(3, user_id=user.id, category_id=category.id)
    )
    session.add_all(TodoFactory.create_batch(2, user_id=user.id))
    await session.commit()

    response = client.get(
        f'/todo/?category_id={category.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    expected_todos = 3
    assert response.status_code == HTTPStatus.OK
    assert len(response.json()['todos']) == expected_todos


@pytest.mark.asyncio
async def test_list_todos_combined_filters(session, client, user, token):
    doing_id = await _status_id(session, 'em_andamento')
    other_id = await _status_id(session, 'nao_iniciada')
    session.add_all(
        TodoFactory.create_batch(
            2,
            user_id=user.id,
            title='Combined title',
            description='combined description',
            status_id=doing_id,
        )
    )
    session.add_all(
        TodoFactory.create_batch(
            3,
            user_id=user.id,
            title='Other title',
            description='other description',
            status_id=other_id,
        )
    )
    await session.commit()

    response = client.get(
        f'/todo/?title=Combined&description=combined&status_id={doing_id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    expected_todos = 2
    assert response.status_code == HTTPStatus.OK
    assert len(response.json()['todos']) == expected_todos


@pytest.mark.asyncio
async def test_patch_todo(session, client, user, token):
    todo = TodoFactory(user_id=user.id)
    session.add(todo)
    await session.commit()
    await session.refresh(todo)

    response = client.patch(
        f'/todo/{todo.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={'title': 'Updated title'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json()['title'] == 'Updated title'
    assert response.json()['description'] == todo.description
    assert response.json()['id'] == todo.id


@pytest.mark.asyncio
async def test_patch_todo_all_fields(
    session, client, user, token, category
):
    todo = TodoFactory(user_id=user.id)
    session.add(todo)
    await session.commit()
    await session.refresh(todo)

    done_id = await _status_id(session, 'concluido')

    response = client.patch(
        f'/todo/{todo.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'title': 'New title',
            'description': 'New description',
            'status_id': done_id,
            'category_id': category.id,
            'issue': 'GH-777',
        },
    )

    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert data['id'] == todo.id
    assert data['title'] == 'New title'
    assert data['description'] == 'New description'
    assert data['status_id'] == done_id
    assert data['category_id'] == category.id
    assert data['issue'] == 'GH-777'


def test_patch_todo_not_found(client, token):
    response = client.patch(
        '/todo/999',
        headers={'Authorization': f'Bearer {token}'},
        json={'title': 'Updated title'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Task not found.'}


@pytest.mark.asyncio
async def test_patch_other_user_todo(session, client, user, other_user, token):
    todo = TodoFactory(user_id=other_user.id)
    session.add(todo)
    await session.commit()
    await session.refresh(todo)

    response = client.patch(
        f'/todo/{todo.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={'title': 'Updated title'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Task not found.'}


def test_patch_todo_without_token(client):
    response = client.patch('/todo/1', json={'title': 'Updated title'})

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Not authenticated'}


@pytest.mark.asyncio
async def test_delete_todo(session, client, user, token):
    todo = TodoFactory(user_id=user.id)
    session.add(todo)
    await session.commit()
    await session.refresh(todo)

    response = client.delete(
        f'/todo/{todo.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'message': 'Task has been deleted successfully.'
    }


def test_delete_todo_not_found(client, token):
    response = client.delete(
        '/todo/999',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Task not found.'}


@pytest.mark.asyncio
async def test_delete_other_user_todo(
    session, client, user, other_user, token
):
    todo = TodoFactory(user_id=other_user.id)
    session.add(todo)
    await session.commit()
    await session.refresh(todo)

    response = client.delete(
        f'/todo/{todo.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Task not found.'}


def test_delete_todo_without_token(client):
    response = client.delete('/todo/1')

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Not authenticated'}


@pytest.mark.asyncio
async def test_todo_invalid_status_fk(session, user):
    todo = TodoFactory(user_id=user.id, status_id=999)
    session.add(todo)

    # status_id sem correspondência em statuses viola a FK no commit.
    with pytest.raises(IntegrityError):
        await session.commit()
