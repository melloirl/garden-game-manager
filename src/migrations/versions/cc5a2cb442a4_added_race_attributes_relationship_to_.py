"""added race attributes + relationship to regions

Revision ID: cc5a2cb442a4
Revises: 90d20445a967
Create Date: 2024-12-23 20:41:12.894418

"""
import sqlmodel
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cc5a2cb442a4'
down_revision: Union[str, None] = '90d20445a967'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('race', sa.Column('base_hp', sa.Float(), nullable=False))
    op.add_column('race', sa.Column('hp_per_level', sa.Float(), nullable=False))
    op.add_column('race', sa.Column('base_mp', sa.Float(), nullable=False))
    op.add_column('race', sa.Column('mp_per_level', sa.Float(), nullable=False))
    op.add_column('race', sa.Column('base_resistance', sa.Float(), nullable=False))
    op.add_column('race', sa.Column('base_strength', sa.Float(), nullable=False))
    op.add_column('race', sa.Column('strength_per_level', sa.Float(), nullable=False))
    op.add_column('race', sa.Column('base_speed', sa.Float(), nullable=False))
    op.add_column('race', sa.Column('speed_per_level', sa.Float(), nullable=False))
    op.add_column('race', sa.Column('created_at', sa.DateTime(), nullable=False))
    op.add_column('race', sa.Column('updated_at', sa.DateTime(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('race', 'updated_at')
    op.drop_column('race', 'created_at')
    op.drop_column('race', 'speed_per_level')
    op.drop_column('race', 'base_speed')
    op.drop_column('race', 'strength_per_level')
    op.drop_column('race', 'base_strength')
    op.drop_column('race', 'base_resistance')
    op.drop_column('race', 'mp_per_level')
    op.drop_column('race', 'base_mp')
    op.drop_column('race', 'hp_per_level')
    op.drop_column('race', 'base_hp')
    # ### end Alembic commands ###