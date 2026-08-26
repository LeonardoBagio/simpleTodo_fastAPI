from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from simple_todo.database import get_session
from simple_todo.models import Todo, User
from simple_todo.schemas import TodoPublic, TodoSchema
from simple_todo.security import get_current_user

router = APIRouter(prefix='/todos', tags=['todos'])

Session = Annotated[AsyncSession, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]


@router.post('/', response_model=TodoPublic)
async def create_todo(
    todo: TodoSchema,
    user: CurrentUser,
    session: Session,
):
    db_todo = Todo(
        user_id=user.id,
        title=todo.title,
        description=todo.description,
        state=todo.state,
    )

    session.add(db_todo)
    await session.commit()
    await session.refresh(db_todo)

    return db_todo
