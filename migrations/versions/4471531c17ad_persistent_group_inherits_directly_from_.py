"""Persistent group inherits directly from intern

Revision ID: 4471531c17ad
Revises: a02fdc6eee57
Create Date: 2016-04-30 01:42:48.290309

"""

# revision identifiers, used by Alembic.
revision = '4471531c17ad'
down_revision = 'a02fdc6eee57'

from alembic import op

from sqlalchemy.sql.elements import quoted_name


def upgrade():
    op.drop_constraint(table_name='persistent_group_list', schema=quoted_name('mail', False),
                       constraint_name='persistent_group_list_id_fkey')
    op.create_foreign_key(
        'persistent_group_list_id_fkey',
        'persistent_group_list', 'intern',
        ['id'], ['id'], source_schema='mail', referent_schema='mail'
    )


def downgrade():
    op.drop_constraint(schema=quoted_name('mail', False), table_name='persistent_group_list',
                       constraint_name='persistent_group_list_id_fkey')
    op.create_foreign_key(
        'persistent_group_list_id_fkey',
        'persistent_group_list', 'list',
        ['id'], ['id'], source_schema='mail', referent_schema='mail'
    )
