"""Added participation requests for sensitive groups

Revision ID: a1ea147bc2d8
Revises: 439aff2edcc9
Create Date: 2016-10-03 17:41:48.884967

"""

# revision identifiers, used by Alembic.
revision = 'a1ea147bc2d8'
down_revision = '439aff2edcc9'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('sensitive_persistent_group_participation_request',
    sa.Column('persistent_group_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['persistent_group_id'], ['general.group.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['general.user.id'], ),
    sa.PrimaryKeyConstraint('persistent_group_id', 'user_id'),
    schema='general'
    )
    op.create_table('sensitive_year_group_participation_request',
    sa.Column('year_group_id', sa.Integer(), nullable=False),
    sa.Column('year_participation_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['year_group_id'], ['general.year_group.id'], ),
    sa.ForeignKeyConstraint(['year_participation_id'], ['general.year_participation.id'], ),
    sa.PrimaryKeyConstraint('year_group_id', 'year_participation_id'),
    schema='general'
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('sensitive_year_group_participation_request', schema='general')
    op.drop_table('sensitive_persistent_group_participation_request', schema='general')
    ### end Alembic commands ###