from datetime import datetime

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column

from simple_todo.models.registry import table_registry


@table_registry.mapped_as_dataclass
class Todo:
    __tablename__ = 'todos'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    title: Mapped[str]
    description: Mapped[str]
    status_id: Mapped[int] = mapped_column(ForeignKey('statuses.id'))
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    category_id: Mapped[int | None] = mapped_column(
        ForeignKey('categories.id'), default=None
    )
    issue: Mapped[str | None] = mapped_column(default=None)
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now(), onupdate=func.now()
    )
