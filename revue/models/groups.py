__author__ = 'fkint'
from sqlalchemy import ForeignKey, PrimaryKeyConstraint

from revue import db


class Group(db.Model):
    __tablename__ = 'group'
    __table_args__ = {'schema': 'general'}
    id = db.Column('id', db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=False)
    type = db.Column(db.String(50), nullable=True)
    __mapper_args__ = {
        'polymorphic_on': type
    }
    def __init__(self, name, description):
        self.name = name
        self.description = description


class YearGroup(Group):
    __tablename__ = "year_group"
    __table_args__ = {"schema": "general"}
    year_group_id = db.Column("id", db.Integer, ForeignKey('general.group.id'), primary_key=True, nullable=False)
    parent_year_group = db.Column(db.Integer, ForeignKey("general.year_group.id"), nullable=True)
    __mapper_args__ = {
        "polymorphic_identity": "year_group"
    }

    def __init__(self, parent_year_group):
        self.parent_year_group = parent_year_group


class GroupParticipation(db.Model):
    __tablename__ = "group_participation"
    __table_args__ = (PrimaryKeyConstraint("group", "user"), {"schema": "general"})
    group = db.Column("group", db.Integer, ForeignKey("general.group.id"), nullable=False)
    user = db.Column("user", db.Integer, ForeignKey("general.user.id"), nullable=False)

    def __init__(self, group, user):
        self.group = group
        self.user = user


class YearGroupParticipation(db.Model):
    __tablename__ = "year_group_participation"
    __table_args__ = (PrimaryKeyConstraint("year", "year_group", "user"), {"schema": "general"})
    year = db.Column("year", db.Integer, ForeignKey("general.revue_year.id"), nullable=False)
    year_group = db.Column("year_group", db.Integer, ForeignKey("general.year_group.id"), nullable=False)
    user = db.Column("user", db.Integer, ForeignKey("general.user.id"), nullable=False)

    def __init__(self, year, year_group, user):
        self.year = year
        self.year_group = year_group
        self.user = user


class RevueYear(db.Model):
    __tablename__ = "revue_year"
    __table_args__ = {"schema": "general"}
    id = db.Column("id", db.Integer, primary_key=True, nullable=False)
    title = db.Column("title", db.String(50), nullable=False)
    year = db.Column("year", db.Integer, nullable=False)

    def __init__(self, title, year):
        self.title = title
        self.year = year
