from sqlalchemy import *

from migrate import *

meta = MetaData()

menu_entry_table = Table(
    'menu_entry', meta,
    Column('id', Integer, nullable=False, primary_key=True),
    Column('title', String(50), nullable=False),
    Column('page', Integer, nullable=False),
    Column('description', Text, nullable=False),

    ForeignKeyConstraint(['page'], ['content.page.id']),
    schema="content"
)

group_menu_table = Table(
    'group_menu', meta,
    Column('menu_entry', Integer, nullable=False),
    Column('group', Integer, nullable=False, primary_key=True),
    ForeignKeyConstraint(['menu_entry'], ['content.menu_entry.id']),
    ForeignKeyConstraint(['group'], ['general.group.id']),
    schema="content"
)

menu_entry_releationship_table = Table(
    'menu_entry_relationship', meta,
    Column('parent', Integer, nullable=False),
    Column('child', Integer, nullable=False),
    ForeignKeyConstraint(['parent'], ['content.menu_entry.id']),
    ForeignKeyConstraint(['child'], ['content.menu_entry.id']),
    PrimaryKeyConstraint('parent', 'child'),
    schema='content'
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    meta.bind = migrate_engine
    Table('group', meta, schema="general", autoload=True)
    Table('page', meta, schema="content", autoload=True)
    menu_entry_table.create()
    group_menu_table.create()
    menu_entry_releationship_table.create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    meta.bind = migrate_engine
    menu_entry_releationship_table.drop()
    group_menu_table.drop()
    menu_entry_table.drop()
