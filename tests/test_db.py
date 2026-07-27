from sqlalchemy import select

from simple_todo.models import User


def test_create_user(session):
    new_user = User(username='teste', email='teste@teste', password='secret')

    session.add(new_user)
    session.commit()

    user = session.scalar(select(User).where(User.username == 'test'))

    # assert user.id == 1
    assert user.username == new_user.username
    assert user.email == new_user.email
    assert user.password == new_user.password
