from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from simple_todo.models.registry import table_registry

if TYPE_CHECKING:
    from simple_todo.models.todo import Todo


@table_registry.mapped_as_dataclass
class User:
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    todos: Mapped[list['Todo']] = relationship(
        init=False,
        cascade='all, delete-orphan',
        lazy='selectin',
    )
