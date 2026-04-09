"""add gist index on buildings location

Revision ID: ea67b58ce1db
Revises: f309cb8a3f9f
Create Date: 2026-04-10 03:41:31.500646

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "ea67b58ce1db"
down_revision: Union[str, Sequence[str], None] = "f309cb8a3f9f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_index("idx_buildings_location_gist", "buildings", ["location"], unique=False, postgresql_using="gist")


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index("idx_buildings_location_gist", table_name="buildings")
