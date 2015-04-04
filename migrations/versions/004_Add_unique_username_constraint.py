from sqlalchemy import *
from migrate.changeset.constraint import UniqueConstraint
meta = MetaData()


def get_user_constraint(meta):
    return UniqueConstraint('username',table=Table('user', meta, schema='general', autoload=True))


def get_registration_constraint(meta):
    return UniqueConstraint('username',table=Table('registration', meta, schema='general', autoload=True))


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    meta.bind = migrate_engine
    user_unique_username = get_user_constraint(meta)
    user_unique_username.create()
    registration_unique_username = get_registration_constraint(meta)
    registration_unique_username.create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    meta.bind = migrate_engine
    user_unique_username = get_user_constraint(meta)
    user_unique_username.drop()
    registration_unique_username = get_registration_constraint(meta)
    registration_unique_username.drop()
