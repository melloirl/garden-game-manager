"""Unambiguos foreign keys in user model

Revision ID: 7e2154df3510
Revises: 5d289f326b68
Create Date: 2024-12-24 03:03:30.660903

"""
import sqlmodel
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7e2154df3510'
down_revision: Union[str, None] = '5d289f326b68'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
