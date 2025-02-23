"""merge code

Revision ID: 8bc198fb391c
Revises: 3e8b58a5465f, 8adfbd478853
Create Date: 2025-02-23 14:29:24.826769

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8bc198fb391c'
down_revision: Union[str, None] = ('3e8b58a5465f', '8adfbd478853')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
