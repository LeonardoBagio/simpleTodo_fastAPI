"""add created_at and updated_at to todos

Revision ID: f1e92e4cd88a
Revises: 8f54e604af4f
Create Date: 2026-08-26 19:11:24.310177

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f1e92e4cd88a'
down_revision: Union[str, Sequence[str], None] = '8f54e604af4f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # SQLite não permite ADD COLUMN com default não-constante via ALTER TABLE,
    # então usamos batch_alter_table (recria a tabela).
    with op.batch_alter_table('todos') as batch_op:
        batch_op.add_column(sa.Column('created_at', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False))
        batch_op.add_column(sa.Column('updated_at', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False))


def downgrade() -> None:
    """Downgrade schema."""
    with op.batch_alter_table('todos') as batch_op:
        batch_op.drop_column('updated_at')
        batch_op.drop_column('created_at')
