"""year group mailing list inherits directly from intern

Revision ID: a02fdc6eee57
Revises: 2476679fb1fa
Create Date: 2016-04-29 18:48:25.219111

"""

# revision identifiers, used by Alembic.
revision = 'a02fdc6eee57'
down_revision = '2476679fb1fa'

import sqlalchemy as sa
from alembic import op


def upgrade():
    op.drop_table('year_group_list', schema='public')
    op.create_table('year_group_list',
                    sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
                    sa.Column('year_group_id', sa.Integer(), nullable=True, unique=True),
                    sa.ForeignKeyConstraint(['year_group_id'], ['general.year_group.id']),
                    sa.ForeignKeyConstraint(['id'], ['mail.intern.id']),
                    schema='mail')


def downgrade():
    op.drop_table('year_group_list', schema='mail')
    op.create_table('year_group_list',
                    sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
                    sa.Column('year_group_id', sa.Integer(), nullable=True, unique=True),
                    sa.ForeignKeyConstraint(['year_group_id'], ['general.year_group.id']),
                    sa.ForeignKeyConstraint(['id'], ['mail.list.id']))
