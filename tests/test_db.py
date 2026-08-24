from dataclasses import asdict
from datetime import datetime

import pytest
from sqlalchemy import select

from simple_todo.models import User


@pytest.mark.asyncio
async def test_create_user(session, mock_db_time):
    with mock_db_time(model=User, time=datetime.now()) as time:
        new_user = User(
            username='teste', email='teste@teste', password='secret'
        )

        session.add(new_user)
        await session.commit()

        user = await session.scalar(
            select(User).where(User.username == 'teste')
        )

    assert asdict(user) == {
        'id': new_user.id,
        'username': new_user.username,
        'email': new_user.email,
        'password': new_user.password,
        'created_at': time,
    }
