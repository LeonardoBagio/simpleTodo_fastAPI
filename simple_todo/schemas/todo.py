from datetime import datetime

from pydantic import BaseModel, Field

from simple_todo.schemas.base import FilterPage


class TodoSchema(BaseModel):
    title: str
    description: str
    # None → o backend resolve o status default ('nao_iniciada').
    status_id: int | None = None
    category_id: int | None = None
    issue: str | None = None


class TodoPublic(BaseModel):
    id: int
    title: str
    description: str
    status_id: int
    category_id: int | None = None
    issue: str | None = None
    created_at: datetime
    updated_at: datetime


class TodoList(BaseModel):
    todos: list[TodoPublic]


class TodoUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    status_id: int | None = None
    category_id: int | None = None
    issue: str | None = None


class FilterTodo(FilterPage):
    title: str | None = Field(None, min_length=3, max_length=20)
    description: str | None = None
    status_id: int | None = None
    category_id: int | None = None
