from sqlalchemy import Table, MetaData,Integer, String, Column
from migrate import PrimaryKeyConstraint, ForeignKeyConstraint


meta = MetaData()
permission = Table(
    'permission', meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('name', String(50), nullable=False),
    schema="general"
)

user_permission = Table(
    'user_permission',
    meta,
    Column('user', Integer, nullable=False),
    Column('permission', Integer,nullable=False),
    ForeignKeyConstraint(['permission'],['general.permission.id']),
    ForeignKeyConstraint(['user'],['general.user.id']),
    PrimaryKeyConstraint('user', 'permission'),
    schema="general"
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    meta.bind = migrate_engine
    user = Table('user', meta, autoload=True, schema='general')

    permission.create()
    user_permission.create()



def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    meta.bind = migrate_engine
    user_permission.drop()
    permission.drop()
