from pydantic import BaseModel, Field

from simple_todo.models import TodoState
from simple_todo.schemas.base import FilterPage


class TodoSchema(BaseModel):
    title: str
    description: str
    state: TodoState = Field(TodoState.todo)


class TodoPublic(TodoSchema):
    id: int


class TodoList(BaseModel):
    todos: list[TodoPublic]


class TodoUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    state: TodoState | None = None


class FilterTodo(FilterPage):
    title: str | None = Field(None, min_length=3, max_length=20)
    description: str | None = None
    state: TodoState | None = None
