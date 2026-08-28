from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from simple_todo.database import get_session
from simple_todo.models import Category, Status, User
from simple_todo.schemas import CategoryList, StatusList
from simple_todo.security import get_current_user

router = APIRouter(prefix='/catalog', tags=['catalog'])

Session = Annotated[AsyncSession, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]


@router.get('/statuses', response_model=StatusList)
async def list_statuses(session: Session, user: CurrentUser):
    statuses = await session.scalars(
        select(Status).order_by(Status.sort_order)
    )
    return {'statuses': statuses.all()}


@router.get('/categories', response_model=CategoryList)
async def list_categories(session: Session, user: CurrentUser):
    categories = await session.scalars(
        select(Category).order_by(Category.sort_order)
    )
    return {'categories': categories.all()}
