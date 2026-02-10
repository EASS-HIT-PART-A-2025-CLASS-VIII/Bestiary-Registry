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
    with op.batch_alter_table("creature") as batch_op:
        batch_op.add_column(
            sa.Column(
                "image_status",
                sqlmodel.sql.sqltypes.AutoString(),
                nullable=False,
                server_default="pending",
            )
        )
        batch_op.add_column(
            sa.Column("image_error", sqlmodel.sql.sqltypes.AutoString(), nullable=True)
        )
        batch_op.alter_column("image_url", existing_type=sa.VARCHAR(), nullable=True)


def downgrade() -> None:
    """Downgrade schema."""
    with op.batch_alter_table("creature") as batch_op:
        batch_op.alter_column("image_url", existing_type=sa.VARCHAR(), nullable=False)
        batch_op.drop_column("image_error")
        batch_op.drop_column("image_status")
