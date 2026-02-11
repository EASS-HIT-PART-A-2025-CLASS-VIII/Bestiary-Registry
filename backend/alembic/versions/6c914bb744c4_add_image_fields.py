"""add_image_fields

Revision ID: 6c914bb744c4
Revises: 034b146bc51b
Create Date: 2026-02-04 09:43:16.387703

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from sqlalchemy import inspect


# revision identifiers, used by Alembic.
revision: str = "6c914bb744c4"
down_revision: Union[str, Sequence[str], None] = "034b146bc51b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    bind = op.get_bind()
    cols = {c["name"] for c in inspect(bind).get_columns("creature")}

    if "image_status" not in cols:
        op.add_column(
            "creature",
            sa.Column(
                "image_status", sa.String(), nullable=False, server_default="pending"
            ),
        )

    if "image_error" not in cols:
        op.add_column(
            "creature",
            sa.Column("image_error", sa.String(), nullable=True),
        )


def downgrade() -> None:
    """Downgrade schema."""
    with op.batch_alter_table("creature") as batch_op:
        batch_op.alter_column("image_url", existing_type=sa.VARCHAR(), nullable=False)
        batch_op.drop_column("image_error")
        batch_op.drop_column("image_status")
