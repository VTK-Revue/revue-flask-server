"""Update group model

Revision ID: 345499a7ce2
Revises: be4990a3b0
Create Date: 2015-11-01 00:36:55.634152

"""

# revision identifiers, used by Alembic.
revision = '345499a7ce2'
down_revision = 'be4990a3b0'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('persistent_group', sa.Column('listed', sa.Boolean(), nullable=False, default=True), schema='general')
    op.add_column('group', sa.Column('sensitive', sa.Boolean(), nullable=False, default=False), schema='general')


def downgrade():
    op.drop_column('persistent_group', 'listed', schema='general')
    op.drop_column('group', 'sensitive', schema='general')
