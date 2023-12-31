"""empty message

Revision ID: 6846ef0ccd9a
Revises: 861f09faff9c
Create Date: 2023-11-16 22:20:36.556485

"""
from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "6846ef0ccd9a"
down_revision: Union[str, None] = "861f09faff9c"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column("session", "device_id", existing_type=sa.INTEGER(), nullable=False)
    op.add_column("shoe", sa.Column("image_url", sa.String(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("shoe", "image_url")
    op.alter_column("session", "device_id", existing_type=sa.INTEGER(), nullable=True)
    # ### end Alembic commands ###
