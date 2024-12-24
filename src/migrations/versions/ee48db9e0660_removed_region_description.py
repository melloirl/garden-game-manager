"""Removed region description

Revision ID: ee48db9e0660
Revises: 6f3fff3d36c5
Create Date: 2024-12-23 20:22:55.213683

"""
import sqlmodel
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = 'ee48db9e0660'
down_revision: Union[str, None] = '6f3fff3d36c5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('region', 'description')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('region', sa.Column('description', mysql.VARCHAR(length=255), nullable=False))
    # ### end Alembic commands ###
