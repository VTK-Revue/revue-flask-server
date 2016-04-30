"""Add list column to list entry table

Revision ID: 5f972f9dcecd
Revises: 4471531c17ad
Create Date: 2016-04-30 03:00:00.814482

"""

# revision identifiers, used by Alembic.
revision = '5f972f9dcecd'
down_revision = '4471531c17ad'

import sqlalchemy as sa
from alembic import op

from sqlalchemy.sql.elements import quoted_name


def upgrade():
    op.drop_table('list_entry', schema='mail')
    op.create_table('list_entry',
                    sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
                    sa.Column('address_id', sa.Integer(), nullable=False),
                    sa.Column('list_id', sa.Integer(), sa.ForeignKey('mail.list.id'), nullable=False),
                    sa.ForeignKeyConstraint(['address_id'], ['mail.address.id']),
                    sa.ForeignKeyConstraint(['list_id'], ['mail.list.id']),
                    schema='mail')

def downgrade():
    op.drop_table('list_entry', schema='mail')
    op.create_table('list_entry',
                    sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
                    sa.Column('address_id', sa.Integer(), nullable=False),
                    sa.Column('type', sa.String(50), nullable=False),
                    sa.ForeignKeyConstraint(['id'], ['mail.address.id']),
                    sa.ForeignKeyConstraint(['address_id'], ['mail.address.id']),
                    schema='mail')