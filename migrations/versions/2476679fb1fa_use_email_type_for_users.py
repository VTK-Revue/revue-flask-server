"""Use email type for users

Revision ID: 2476679fb1fa
Revises: b4ca29ea5e42
Create Date: 2016-04-17 22:35:44.287669

"""

# revision identifiers, used by Alembic.
revision = '2476679fb1fa'
down_revision = 'b4ca29ea5e42'

import sqlalchemy as sa
from alembic import op


def upgrade():
    op.add_column('user', sa.Column('email_address_id', sa.INTEGER, sa.ForeignKey('mail.extern_address.id')),
                  schema='general')
    op.drop_column('user', 'email', schema='general')


def downgrade():
    op.drop_column('user', 'email_address_id', schema='general')
    op.add_column('user', sa.Column('email', sa.String(length=100), nullable=True), schema='general')
