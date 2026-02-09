"""add_image_fields

Revision ID: 6c914bb744c4
Revises: 034b146bc51b
Create Date: 2026-02-04 09:43:16.387703

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = "6c914bb744c4"
down_revision: Union[str, Sequence[str], None] = "034b146bc51b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "creature",
        sa.Column(
            "image_status",
            sqlmodel.sql.sqltypes.AutoString(),
            nullable=False,
            server_default="pending",
        ),
    )
    op.add_column(
        "creature",
        sa.Column("image_error", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    )
    op.alter_column("creature", "image_url", existing_type=sa.VARCHAR(), nullable=True)
    # op.drop_constraint(op.f('uq_creature_name'), 'creature', type_='unique')


def downgrade() -> None:
    """Downgrade schema."""
    # op.create_unique_constraint(op.f('uq_creature_name'), 'creature', ['name'], postgresql_nulls_not_distinct=False)
    op.alter_column("creature", "image_url", existing_type=sa.VARCHAR(), nullable=False)
    op.drop_column("creature", "image_error")
    op.drop_column("creature", "image_status")
