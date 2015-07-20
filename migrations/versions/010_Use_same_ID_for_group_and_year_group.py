from sqlalchemy import *

from migrate import *

meta = MetaData()


def get_table(meta):
    return Table('year_group', meta, schema='general', autoload=True)

def get_old_constraint(meta):
    return ForeignKeyConstraint(['group'],['general.group.id'], table=get_table(meta))


def get_new_constraint(meta):
    return ForeignKeyConstraint(['id'], ['general.group.id'], table=get_table(meta))


def get_old_column():
    return Column('group', Integer)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    meta.bind = migrate_engine
    get_old_constraint(meta).drop()
    get_old_column().drop(get_table(meta))
    get_new_constraint(meta).create()



def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    meta.bind = migrate_engine
    get_new_constraint(meta).drop()
    get_old_column().create(get_table(meta))
    get_old_constraint(meta).create()
