"""add indexes on price ticker and date

Revision ID: a7995f12fd6d
Revises: 0ed077a26c04
Create Date: 2026-06-04 20:04:55.553571

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a7995f12fd6d'
down_revision: Union[str, Sequence[str], None] = '0ed077a26c04'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_index('ix_price_ticker', 'price', ['ticker'])
    op.create_index('ix_price_date', 'price', ['date'])
    pass


def downgrade() -> None:
    op.drop_index('ix_price_ticker', 'price')
    op.drop_index('ix_price_date', 'price')
    """Downgrade schema."""
    pass
