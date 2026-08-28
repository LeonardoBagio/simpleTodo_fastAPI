from pydantic import BaseModel


class StatusPublic(BaseModel):
    id: int
    code: str
    label: str
    color: str
    group: str
    sort_order: int


class CategoryPublic(BaseModel):
    id: int
    code: str
    label: str
    color: str
    sort_order: int


class StatusList(BaseModel):
    statuses: list[StatusPublic]


class CategoryList(BaseModel):
    categories: list[CategoryPublic]
