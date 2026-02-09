"""add_tags

Revision ID: 034b146bc51b
Revises: 215b50182062
Create Date: 2026-02-03 20:18:14.182951

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = "034b146bc51b"
down_revision: Union[str, Sequence[str], None] = "215b50182062"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Ensure name is unique for ForeignKey to work
    op.create_unique_constraint("uq_creature_name", "creature", ["name"])

    op.create_table(
        "tag",
        sa.Column("name", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.PrimaryKeyConstraint("name"),
    )
    op.create_table(
        "creaturetaglink",
        sa.Column("creature_name", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("tag_name", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.ForeignKeyConstraint(
            ["creature_name"],
            ["creature.name"],
        ),
        sa.ForeignKeyConstraint(
            ["tag_name"],
            ["tag.name"],
        ),
        sa.PrimaryKeyConstraint("creature_name", "tag_name"),
    )


def downgrade() -> None:
    op.drop_table("creaturetaglink")
    op.drop_table("tag")
    op.drop_constraint("uq_creature_name", "creature", type_="unique")
