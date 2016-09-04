"""Add year group year pages

Revision ID: 439aff2edcc9
Revises: 5b0e7c9084af
Create Date: 2016-09-04 16:01:15.245707

"""

# revision identifiers, used by Alembic.
revision = '439aff2edcc9'
down_revision = '5b0e7c9084af'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table('year_group_year_page',
    sa.Column('year_group_id', sa.Integer(), nullable=False),
    sa.Column('year_id', sa.Integer(), nullable=False),
    sa.Column('page_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['page_id'], ['content.page.id'], ),
    sa.ForeignKeyConstraint(['year_group_id'], ['general.year_group.id'], ),
    sa.ForeignKeyConstraint(['year_id'], ['general.revue_year.id'], ),
    sa.PrimaryKeyConstraint('year_group_id', 'year_id'),
    schema='content'
    )


def downgrade():
    op.drop_table('year_group_year_page', schema='content')
