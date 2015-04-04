from sqlalchemy import Boolean,Table, Column,Integer,String, Text,MetaData
from migrate import ForeignKeyConstraint, PrimaryKeyConstraint, UniqueConstraint
meta = MetaData()
page = Table(
    'page', meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('url_identifier', String(50), nullable=False),
    Column('title', String(50), nullable=False),
    Column('parent_page', Integer, nullable=True),
    Column('description', Text, nullable=False),
    Column('access_restricted',Boolean,nullable=False),
    ForeignKeyConstraint(['parent_page'],['content.page.id']),
    UniqueConstraint('parent_page', 'url_identifier'),
    schema="content"
)

page_access_restriction = Table(
    'page_access_restriction',
    meta,
    Column('page', Integer, nullable=False),
    Column('year_group', Integer,nullable=False),
    Column('revue_year', Integer, nullable=False),
    ForeignKeyConstraint(['page'], ['content.page.id']),
    ForeignKeyConstraint(['year_group'], ['general.year_group.id']),
    ForeignKeyConstraint(['revue_year'],['general.revue_year.id']),
    PrimaryKeyConstraint('page', 'year_group', 'revue_year'),
    schema="content"
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    meta.bind = migrate_engine
    user = Table('user', meta, autoload=True, schema='general')
    year_group = Table("year_group", meta, autoload=True, schema="general")
    revue_year = Table("revue_year", meta, autoload=True, schema="general")
    page.create()
    page_access_restriction.create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    meta.bind = migrate_engine
    page_access_restriction.drop()
    page.drop()
