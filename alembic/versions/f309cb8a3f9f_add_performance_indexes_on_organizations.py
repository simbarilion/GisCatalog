"""add performance indexes on organizations

Revision ID: f309cb8a3f9f
Revises: 5bc1f2fc7bfb
Create Date: 2026-04-10 03:25:13.230800

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "f309cb8a3f9f"
down_revision: Union[str, Sequence[str], None] = "5bc1f2fc7bfb"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_index("idx_org_name", "organizations", ["name"], unique=False)

    op.create_index("idx_org_building_id", "organizations", ["building_id"], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index("idx_org_name", table_name="organizations")
    op.drop_index("idx_org_building_id", table_name="organizations")
