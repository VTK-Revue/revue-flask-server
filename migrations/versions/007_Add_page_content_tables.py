from sqlalchemy import Column, Table, Enum, Integer, Text, MetaData, Boolean, String
from migrate import ForeignKeyConstraint, PrimaryKeyConstraint, UniqueConstraint


meta = MetaData()

content_element = Table(
    'content_element', meta,
    Column('id', Integer, nullable=False, primary_key=True),
    Column('type', Enum('text', 'container', 'vuedle', 'announcement', name="content_element_types"), nullable=False),
    Column('sticky', Boolean, nullable=False, default=False),
    Column('title', String(50), nullable=False, default=""),
    Column('identifier', String(50), nullable=False, default=None),
    Column('author', Integer, nullable=False),
    ForeignKeyConstraint(['author'], ['general.user.id']),
    schema="content"
)

page_content_element = Table(
    'page_content_element', meta,
    Column('content_element', Integer, nullable=False),
    Column('page', Integer, nullable=False),
    Column('order_index', Integer, nullable=False, default=0),
    PrimaryKeyConstraint('content_element', 'page'),
    ForeignKeyConstraint(['content_element'], ['content.content_element.id']),
    ForeignKeyConstraint(['page'], ['content.page.id']),
    schema="content"
)

text_element = Table(
    'text_element', meta,
    Column('id', Integer, nullable=False, primary_key=True),
    Column('content_element', Integer, nullable=False),
    Column('content', Text, nullable=False),
    ForeignKeyConstraint(['content_element'], ['content.content_element.id']),
    schema="content"
)



def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    meta.bind = migrate_engine
    page = Table('page', meta, schema="content", autoload=True)
    user = Table('user', meta, schema="general", autoload=True)

    content_element.create();
    page_content_element.create()
    text_element.create()



def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    meta.bind = migrate_engine

    text_element.drop()
    page_content_element.drop()
    content_element.drop()
