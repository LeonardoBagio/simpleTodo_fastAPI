from sqlalchemy.orm import Mapped, mapped_column

from simple_todo.models.registry import table_registry


@table_registry.mapped_as_dataclass
class Category:
    """Cadastro global de Categoria (seeded). Compartilhado entre usuários."""

    __tablename__ = 'categories'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    code: Mapped[str] = mapped_column(unique=True)
    label: Mapped[str]
    color: Mapped[str]
    sort_order: Mapped[int]
