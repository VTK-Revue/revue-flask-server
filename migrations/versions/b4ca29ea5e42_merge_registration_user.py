"""Merge registration/user

Revision ID: b4ca29ea5e42
Revises: 7d4dc8213cf3
Create Date: 2016-04-10 22:44:27.373245

"""

# revision identifiers, used by Alembic.
revision = 'b4ca29ea5e42'
down_revision = '7d4dc8213cf3'

import sqlalchemy as sa
from alembic import op


def upgrade():
    op.add_column('user', sa.Column('activated', sa.DateTime(), nullable=True, default=None), schema='general')
    op.drop_table('registration', schema='general')


def downgrade():
    op.create_table('registration',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('firstName', sa.String(length=60), nullable=True),
                    sa.Column('lastName', sa.String(length=60), nullable=True),
                    sa.Column('email', sa.String(length=100), nullable=True),
                    sa.Column('username', sa.String(length=20), nullable=True),
                    sa.Column('password', sa.String(length=60), nullable=True),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('username'),
                    schema='general'
                    )
    op.drop_column('user', 'activated', schema='general')
