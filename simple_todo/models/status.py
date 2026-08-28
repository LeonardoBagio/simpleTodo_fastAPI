from sqlalchemy.orm import Mapped, mapped_column

from simple_todo.models.registry import table_registry


@table_registry.mapped_as_dataclass
class Status:
    """Cadastro global de Andamento (seeded). Compartilhado entre usuários."""

    __tablename__ = 'statuses'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    code: Mapped[str] = mapped_column(unique=True)
    label: Mapped[str]
    color: Mapped[str]
    # Grupo do ciclo de vida: a_fazer | em_andamento | concluidos
    group: Mapped[str]
    sort_order: Mapped[int]
