"""Add mail schema

Revision ID: 7d4dc8213cf3
Revises: 74f13a6e523e
Create Date: 2016-04-10 16:09:33.259088

"""

# revision identifiers, used by Alembic.
revision = '7d4dc8213cf3'
down_revision = '345499a7ce2'

import sqlalchemy as sa
from alembic import op


def upgrade():
    op.create_table('address',
                    sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
                    sa.Column('type', sa.String(50), nullable=True),
                    schema='mail')
    op.create_table('intern',
                    sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
                    sa.Column('name', sa.String(50), unique=True, nullable=False),
                    sa.ForeignKeyConstraint(['id'], ['mail.address.id']),
                    schema='mail')
    op.create_table('list',
                    sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
                    sa.ForeignKeyConstraint(['id'], ['mail.intern.id']),
                    schema='mail')
    op.create_table('persistent_group_list',
                    sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
                    sa.Column('persistent_group_id', sa.Integer(), nullable=True, unique=True),
                    sa.ForeignKeyConstraint(['persistent_group_id'], ['general.persistent_group.id']),
                    sa.ForeignKeyConstraint(['id'], ['mail.list.id']),
                    schema='mail')
    op.create_table('year_group_list',
                    sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
                    sa.Column('year_group_id', sa.Integer(), nullable=True, unique=True),
                    sa.ForeignKeyConstraint(['year_group_id'], ['general.year_group.id']),
                    sa.ForeignKeyConstraint(['id'], ['mail.list.id']))
    op.create_table('alias',
                    sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
                    sa.Column('other_address_id', sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(['id'], ['mail.address.id']),
                    sa.ForeignKeyConstraint(['other_address_id'], ['mail.intern.id']),
                    schema='mail')
    op.create_table('local_address',
                    sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
                    sa.ForeignKeyConstraint(['id'], ['mail.intern.id']),
                    schema='mail')
    op.create_table('extern_address',
                    sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
                    sa.Column('address', sa.String(150), nullable=False),
                    sa.ForeignKeyConstraint(['id'], ['mail.address.id']),
                    schema='mail')
    op.create_table('list_entry',
                    sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
                    sa.Column('address_id', sa.Integer(), nullable=False),
                    sa.Column('type', sa.String(50), nullable=False),
                    sa.ForeignKeyConstraint(['id'], ['mail.address.id']),
                    sa.ForeignKeyConstraint(['address_id'], ['mail.address.id']),
                    schema='mail')


def downgrade():
    op.drop_table('list_entry', schema='mail')
    op.drop_table('extern_address', schema='mail')
    op.drop_table('local_address', schema='mail')
    op.drop_table('alias', schema='mail')
    op.drop_table('year_group_list', schema='mail')
    op.drop_table('persistent_group_list', schema='mail')
    op.drop_table('list', schema='mail')
    op.drop_table('intern', schema='mail')
    op.drop_table('address', schema='mail')
