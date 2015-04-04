from sqlalchemy import *
from migrate import *
meta = MetaData()
group = Table(
    'group', meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('name', String(50), nullable=False),
    Column('description', Text, nullable=False),
    schema="general"
)

year_group = Table(
    'year_group',
    meta,
    Column('id', Integer, nullable=False,primary_key=True),
    Column('name', String(50),nullable=False),
    Column('description', Text, nullable=False),
    Column('parent_year_group', Integer, nullable=True),
    ForeignKeyConstraint(['parent_year_group'], ['general.year_group.id']),
    schema="general"
)

group_participation = Table(
    'group_participation',
    meta,
    Column('group', Integer, nullable=False),
    Column('user', Integer, nullable=False),
    PrimaryKeyConstraint('group', 'user'),
    ForeignKeyConstraint(['group'], ['general.group.id']),
    ForeignKeyConstraint(['user'], ['general.user.id']),
    schema="general"
)

year_group_participation = Table(
    'year_group_participation',
    meta,
    Column('year', Integer, nullable=False),
    Column('year_group', Integer, nullable=False),
    Column('user', Integer, nullable=False),
    ForeignKeyConstraint(['user'], ['general.user.id']),
    ForeignKeyConstraint(['year_group'], ['general.year_group.id']),
    ForeignKeyConstraint(['year'], ['general.revue_year.id']),
    PrimaryKeyConstraint('year', 'year_group', 'user'),
    schema="general"
)

revue_year = Table(
    'revue_year',
    meta,
    Column('id', Integer, nullable=False, primary_key=True),
    Column('title', String(150), nullable=False),
    Column('year', Integer, nullable=False),
    schema="general"
)

def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    meta.bind = migrate_engine
    user = Table('user', meta, autoload=True, schema='general')
    revue_year.create()
    group.create()
    year_group.create()
    year_group_participation.create()
    group_participation.create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    meta.bind = migrate_engine
    group_participation.drop()
    year_group_participation.drop()
    year_group.drop()
    group.drop()
    revue_year.drop()
