"""Create YearParticipation

Revision ID: 5b0e7c9084af
Revises: 5f972f9dcecd
Create Date: 2016-07-13 06:34:49.740769

"""

import sqlalchemy as sa
from alembic import op
from sqlalchemy.sql.elements import quoted_name
from sqlalchemy.sql.expression import text

# revision identifiers, used by Alembic.
revision = '5b0e7c9084af'
down_revision = '5f972f9dcecd'

USER_ID = 0
YEAR_ID = 1
YEAR_GROUP_ID = 2


def get_old_year_group_participations(connection):
    s = text("SELECT user_id, year_id, year_group_id FROM general.year_group_participation WHERE TRUE")
    year_group_participations = connection.execute(s).fetchall()
    year_participations = dict()
    current_id = 1
    entries = []
    for ygp in year_group_participations:
        user = ygp[USER_ID]
        year = ygp[YEAR_ID]
        key = (user, year)
        if key not in year_participations:
            year_participations[key] = current_id
            current_id += 1
        entries.append((year_participations[key], ygp[YEAR_GROUP_ID]))
    return year_participations, entries


def clear_year_group_participations(connection):
    d = text("DELETE FROM general.year_group_participation WHERE TRUE")
    connection.execute(d)


def insert_new_year_group_participations(connection, year_participations, year_group_participations):
    i_ygp = text("INSERT INTO general.year_group_participation (year_participation_id, year_group_id) VALUES(:ypi, :gi)")
    i_ypr = text("INSERT INTO general.year_participation_request(id, year_id, user_id) VALUES(:ypri, :yi, :ui)")
    i_yp = text("INSERT INTO general.year_participation(id) VALUES(:id)")
    for key, ypr_id in year_participations.items():
        connection.execute(i_ypr, ypri=ypr_id, yi=key[1], ui=key[0])
        connection.execute(i_yp, id=ypr_id)
    for e in year_group_participations:
        connection.execute(i_ygp, ypi=e[0], gi=e[1])


def upgrade():
    # New table year_participation_request
    op.create_table('year_participation_request',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('year_id', sa.Integer(), nullable=False),
                    sa.Column('user_id', sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(['user_id'], ['general.user.id'], ),
                    sa.ForeignKeyConstraint(['year_id'], ['general.revue_year.id'], ),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('year_id', 'user_id'),
                    schema='general'
                    )
    # New table year_participation
    op.create_table('year_participation',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(['id'], ['general.year_participation_request.id'], ),
                    sa.PrimaryKeyConstraint('id'),
                    schema='general'
                    )

    connection = op.get_bind()
    # Data migration
    year_participations, year_group_participations = get_old_year_group_participations(connection)
    clear_year_group_participations(connection)

    # Modified table year_group_participation
    # Remove primary key
    op.drop_constraint(schema=quoted_name('general', False), table_name='year_group_participation',
                       constraint_name='year_group_participation_pkey')
    # Remove user_id
    op.drop_constraint(schema=quoted_name('general', False), table_name='year_group_participation',
                       constraint_name='year_group_participation_user_id_fkey')
    op.drop_column('year_group_participation', 'user_id', schema='general')
    # Remove year_id
    op.drop_constraint(schema=quoted_name('general', False), table_name='year_group_participation',
                       constraint_name='year_group_participation_year_id_fkey')
    op.drop_column('year_group_participation', 'year_id', schema='general')

    # Add column year_participation_id
    op.add_column('year_group_participation',
                  sa.Column('year_participation_id', sa.Integer(), nullable=False), schema='general')
    op.create_foreign_key(
        'year_group_participation_year_participation_id_fkey',
        'year_group_participation', 'year_participation',
        ['year_participation_id'], ['id'], source_schema='general', referent_schema='general'
    )
    # Add primary key
    op.create_primary_key('year_group_participation_pkey', 'year_group_participation',
                          ['year_group_id', 'year_participation_id'], schema='general')

    # Data migration
    insert_new_year_group_participations(connection, year_participations, year_group_participations)


def downgrade():
    connection = op.get_bind()
    # Data migration
    year_participations = dict()
    s1 = text("SELECT id, year_id, user_id FROM general.year_participation_request")
    year_participations_data = connection.execute(s1).fetchall()
    for yp in year_participations_data:
        # [id] = (user, year)
        year_participations[yp[0]] = (yp[2], yp[1])
    s2 = text("SELECT year_group_id, year_participation_id FROM general.year_group_participation")
    year_group_participations_data = connection.execute(s2).fetchall()
    year_group_participations = []
    for ygp in year_group_participations_data:
        yp = year_participations[ygp[1]]
        # (user, year, group)
        year_group_participations.append((yp[0], yp[1], ygp[0]))
    d = text("DELETE FROM general.year_group_participation WHERE TRUE")
    connection.execute(d)

    # Modified table year_group_participation
    # Remove primary key
    op.drop_constraint(schema=quoted_name('general', False), table_name='year_group_participation',
                       constraint_name='year_group_participation_pkey')
    # Remove year_participation_id
    op.drop_constraint(schema=quoted_name('general', False), table_name='year_group_participation',
                       constraint_name='year_group_participation_year_participation_id_fkey')
    op.drop_column('year_group_participation', 'year_participation_id', schema='general')
    # Add user_id
    op.add_column('year_group_participation', sa.Column('user_id', sa.Integer(), nullable=False), schema='general')  # user_id
    op.create_foreign_key(
        'year_group_participation_user_id_fkey', 'year_group_participation', 'user',
        ['user_id'], ['id'], source_schema='general', referent_schema='general'
    )
    # Add year_id
    op.add_column('year_group_participation', sa.Column('year_id', sa.Integer(), nullable=False), schema='general')  # year_id
    op.create_foreign_key(
        'year_group_participation_year_id_fkey', 'year_group_participation', 'revue_year',
        ['year_id'], ['id'], source_schema='general', referent_schema='general'
    )
    # Add primary key
    op.create_primary_key('year_group_participation_pkey', 'year_group_participation',
                          ['year_id', 'year_group_id', 'user_id'], schema='general')

    # Delete new table year_participation
    op.drop_table('year_participation', schema='general')
    # Delete new table year_participation_request
    op.drop_table('year_participation_request', schema='general')

    # Data migration
    i = text("INSERT INTO general.year_group_participation(year_id, user_id, year_group_id) VALUES (:yi, :ui, :ygi)")
    for e in year_group_participations:
        connection.execute(i, yi=e[1], ui=e[0], ygi=e[2])

