"""status/category cadastros, issue field, drop state enum

Revision ID: c2f7a9b1d3e4
Revises: f1e92e4cd88a
Create Date: 2026-08-28 11:00:00.000000

"""
from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'c2f7a9b1d3e4'
down_revision: Union[str, Sequence[str], None] = 'f1e92e4cd88a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


# Cópia estática do seed (ver simple_todo/seeds.py). Migrations devem ser
# imutáveis, por isso os dados ficam embutidos aqui.
STATUSES = [
    ('nao_iniciada', 'Não iniciada', '#9b9a97', 'a_fazer', 1),
    ('stand_by', 'Stand by', '#cb7e3a', 'a_fazer', 2),
    ('aguardando_retorno', 'Aguardando retorno', '#dfab01', 'a_fazer', 3),
    ('code_review', 'Code-review', '#e03e3e', 'em_andamento', 4),
    ('em_andamento', 'Em andamento', '#337ea9', 'em_andamento', 5),
    ('pronto_para_homologar', 'Pronto para homologar', '#c1558b', 'em_andamento', 6),  # noqa: E501
    ('homologacao', 'Homologação', '#9065b0', 'em_andamento', 7),
    ('concluido', 'Concluído', '#448361', 'concluidos', 8),
]

CATEGORIES = [
    ('hotfix', 'hotfix', '#b8496b', 1),
    ('feature', 'feature', '#337ea9', 2),
    ('data_conversion', 'data conversion', '#c1912e', 3),
    ('release', 'Release', '#448361', 4),
    ('task', 'Task', '#9065b0', 5),
    ('epic', 'Epic', '#c1558b', 6),
    ('sub_issue', 'sub issue', '#8a6ea6', 7),
    ('orientacao', 'Orientação', '#9b9a97', 8),
]


def upgrade() -> None:
    """Upgrade schema."""
    statuses = op.create_table(
        'statuses',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('code', sa.String(), nullable=False),
        sa.Column('label', sa.String(), nullable=False),
        sa.Column('color', sa.String(), nullable=False),
        sa.Column('group', sa.String(), nullable=False),
        sa.Column('sort_order', sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('code'),
    )
    categories = op.create_table(
        'categories',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('code', sa.String(), nullable=False),
        sa.Column('label', sa.String(), nullable=False),
        sa.Column('color', sa.String(), nullable=False),
        sa.Column('sort_order', sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('code'),
    )

    op.bulk_insert(
        statuses,
        [
            {
                'code': code,
                'label': label,
                'color': color,
                'group': group,
                'sort_order': order,
            }
            for (code, label, color, group, order) in STATUSES
        ],
    )
    op.bulk_insert(
        categories,
        [
            {
                'code': code,
                'label': label,
                'color': color,
                'sort_order': order,
            }
            for (code, label, color, order) in CATEGORIES
        ],
    )

    # Novas colunas na tarefa (status_id nullable por enquanto).
    op.add_column('todos', sa.Column('status_id', sa.Integer(), nullable=True))
    op.add_column(
        'todos', sa.Column('category_id', sa.Integer(), nullable=True)
    )
    op.add_column('todos', sa.Column('issue', sa.String(), nullable=True))

    # Mapeia o antigo state → status_id.
    op.execute(
        """
        UPDATE todos SET status_id = s.id
        FROM statuses s
        WHERE s.code = CASE todos.state::text
            WHEN 'draft' THEN 'nao_iniciada'
            WHEN 'todo' THEN 'nao_iniciada'
            WHEN 'doing' THEN 'em_andamento'
            WHEN 'done' THEN 'concluido'
            WHEN 'trash' THEN 'concluido'
            ELSE 'nao_iniciada'
        END
        """
    )

    op.create_foreign_key(
        'todos_status_id_fkey', 'todos', 'statuses', ['status_id'], ['id']
    )
    op.create_foreign_key(
        'todos_category_id_fkey',
        'todos',
        'categories',
        ['category_id'],
        ['id'],
    )
    op.alter_column('todos', 'status_id', nullable=False)

    op.drop_column('todos', 'state')
    sa.Enum(name='todostate').drop(op.get_bind(), checkfirst=True)


def downgrade() -> None:
    """Downgrade schema."""
    todostate = sa.Enum(
        'draft', 'todo', 'doing', 'done', 'trash', name='todostate'
    )
    todostate.create(op.get_bind(), checkfirst=True)
    op.add_column(
        'todos',
        sa.Column('state', todostate, nullable=True),
    )

    # Reconstrói um state aproximado a partir do grupo do status.
    op.execute(
        """
        UPDATE todos SET state = (
            CASE s.group
                WHEN 'em_andamento' THEN 'doing'
                WHEN 'concluidos' THEN 'done'
                ELSE 'draft'
            END
        )::todostate
        FROM statuses s
        WHERE s.id = todos.status_id
        """
    )
    op.alter_column('todos', 'state', nullable=False)

    op.drop_constraint('todos_category_id_fkey', 'todos', type_='foreignkey')
    op.drop_constraint('todos_status_id_fkey', 'todos', type_='foreignkey')
    op.drop_column('todos', 'issue')
    op.drop_column('todos', 'category_id')
    op.drop_column('todos', 'status_id')

    op.drop_table('categories')
    op.drop_table('statuses')
