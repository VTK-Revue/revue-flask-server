from sqlalchemy import *
from migrate import *

meta = MetaData()


group_column = Column('group', Integer, nullable=False)
def get_constraint(meta):
    return ForeignKeyConstraint(['group'], ['general.group.id'], table=get_table(meta))

def get_table(meta):
    return Table('year_group', meta, schema='general', autoload=True)

description_column = Column('description', Text, nullable=False)
name_column = Column('name', String(50), nullable=False)
def get_group_table(meta):
    return Table('group', meta, schema="general", autoload=True)

type_column = Column('type', String(50), nullable=True)

def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    meta.bind = migrate_engine
    type_column.create(get_group_table(meta))
    name_column.drop(get_table(meta))
    description_column.drop(get_table(meta))
    group_column.create(get_table(meta))
    get_constraint(meta).create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    meta.bind = migrate_engine
    get_constraint(meta).drop()
    group_column.drop(get_table(meta))
    name_column.create(get_table(meta))
    type_column.drop(get_group_table(meta))
    description_column.create(get_table(meta))


