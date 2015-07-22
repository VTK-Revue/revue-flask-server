__author__ = 'Floris Kint'

from revue import db
from sqlalchemy import ForeignKey, PrimaryKeyConstraint


class MenuEntry(db.Model):
    __tablename__ = "menu_entry"
    __table_args__ = {"schema": "content"}

    id = db.Column("id", db.Integer, primary_key=True, nullable=False)
    title = db.Column("title", db.String(50), nullable=False)
    page = db.Column("page", db.Integer, ForeignKey('content.page.id'), nullable=False)
    description = db.Column("description", db.Text, nullable=False, default='')

    def __init__(self, title, page, description):
        self.title = title
        self.page = page
        self.description = description


class GroupMenu(db.Model):
    __tablename__ = "group_menu"
    __table_args__ = {"schema": "content"}

    menu_entry_id = db.Column('menu_entry', db.Integer, ForeignKey('content.menu_entry.id'), nullable=False)
    group_id = db.Column('group', db.Integer, ForeignKey('general.group.id'), primary_key=True)

    def __init__(self, menu_entry_id, group_id):
        self.menu_entry_id = menu_entry_id
        self.group_id = group_id


class MenuEntryRelationship(db.Model):
    __tablename__ = "menu_entry_relationship"
    __table_args__ = (PrimaryKeyConstraint('parent', 'child'), {"schema": "content"})

    child_id = db.Column('child', db.Integer, ForeignKey('content.menu_entry.id'), nullable=False)
    parent_id = db.Column('parent', db.Integer, ForeignKey('content.menu_entry.id'), nullable=False)

    def __init__(self, parent_id, child_id):
        self.child_id = child_id
        self.parent_id = parent_id

