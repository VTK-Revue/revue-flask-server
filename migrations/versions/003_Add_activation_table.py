from sqlalchemy import Table, Column, String, Integer, MetaData

meta = MetaData()
registration = Table(
    'registration', meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('firstName', String(60), nullable=False),
    Column('lastName', String(60), nullable=False),
    Column('email', String(100), nullable=False),
    Column('username', String(20), nullable=False),
    Column('password', String(60), nullable=False),

    schema="general"
)
def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    meta.bind = migrate_engine
    registration.create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    meta.bind=migrate_engine
    registration.drop()
