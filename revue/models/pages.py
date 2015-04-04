__author__ = 'fkint'
from revue import db

from sqlalchemy import ForeignKey, PrimaryKeyConstraint,UniqueConstraint

class Page(db.Model):
    __tablename__ = 'page'
    __table_args__ = (UniqueConstraint('parent_page', 'url_identifier'),{'schema': 'content'})
    id = db.Column('id', db.Integer, primary_key=True,nullable=False)
    title = db.Column(db.String(50), nullable =False)
    parent_page = db.Column("parent_page", db.Integer, ForeignKey("content.page.id"), nullable=True)
    description = db.Column(db.Text, nullable=False)
    access_restricted = db.Column("access_restricted", db.Boolean, nullable=False)
    url_identifier = db.Column('url_identifier', db.String(50), nullable=False)

    def __init__(self, name, parent_page, description, access_restricted):
        self.name = name
        self.parent_page = parent_page
        self.description = description
        self.access_restricted = access_restricted


class PageAccessRestriction(db.Model):
    __tablename__ = "page_access_restriction"
    __table_args__ = (PrimaryKeyConstraint("page", "year_group", "revue_year"),{"schema":"content"})
    page = db.Column("page", db.Integer, ForeignKey("content.page.id"), nullable=False)
    year_group = db.Column("year_group", db.Integer, ForeignKey("general.year_group.id"), nullable=False)
    revue_year = db.Column("revue_year", db.Integer, ForeignKey("general.revue_year.id"), nullable=False)

    def __init__(self, page, year_group, revue_year):
        self.page = page
        self.year_group = year_group
        self.revue_year = revue_year
