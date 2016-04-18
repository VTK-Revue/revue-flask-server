from sqlalchemy import ForeignKey, PrimaryKeyConstraint

from revue import db
import revue.models.general
import revue.models.mail


class Group(db.Model):
    __tablename__ = 'group'
    __table_args__ = {'schema': 'general'}
    id = db.Column('id', db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=False)
    type = db.Column(db.String(50), nullable=True)
    sensitive = db.Column(db.Boolean(), nullable=False, default=False)
    __mapper_args__ = {
        'polymorphic_on': type
    }


class PersistentGroup(Group):
    __tablename__ = "persistent_group"
    __table_args__ = {"schema": "general"}
    persistent_group_id = db.Column("id", db.Integer, ForeignKey('general.group.id'), primary_key=True, nullable=False)
    parent_persistent_group_id = db.Column(db.Integer, ForeignKey("general.persistent_group.id"), nullable=True)
    listed = db.Column(db.Boolean, nullable=False, default=True)
    __mapper_args__ = {
        "polymorphic_identity": "persistent_group"
    }

    def mailing_list(self):
        return revue.models.mail.PersistentGroupMailingList.query.filter_by(persistent_group_id=self.persistent_group_id).one_or_none()

    def members(self):
        return [revue.models.general.User.query.get(pgp.user_id) for pgp in PersistentGroupParticipation.query.filter_by(group_id = self.id)]


class YearGroup(Group):
    __tablename__ = "year_group"
    __table_args__ = {"schema": "general"}
    year_group_id = db.Column("id", db.Integer, ForeignKey('general.group.id'), primary_key=True, nullable=False)
    parent_year_group_id = db.Column("parent_year_group_id", db.Integer, ForeignKey("general.year_group.id"),
                                     nullable=True)
    __mapper_args__ = {
        "polymorphic_identity": "year_group"
    }


class PersistentGroupParticipation(db.Model):
    __tablename__ = "persistent_group_participation"
    __table_args__ = (PrimaryKeyConstraint("persistent_group_id", "user_id"), {"schema": "general"})
    group_id = db.Column("persistent_group_id", db.Integer, ForeignKey("general.group.id"), nullable=False)
    user_id = db.Column("user_id", db.Integer, ForeignKey("general.user.id"), nullable=False)

    def __init__(self, persistent_group_id, user_id):
        self.group_id = persistent_group_id
        self.user_id = user_id


class YearGroupParticipation(db.Model):
    __tablename__ = "year_group_participation"
    __table_args__ = (PrimaryKeyConstraint("year_id", "year_group_id", "user_id"), {"schema": "general"})
    year_id = db.Column("year_id", db.Integer, ForeignKey("general.revue_year.id"), nullable=False)
    group_id = db.Column("year_group_id", db.Integer, ForeignKey("general.year_group.id"), nullable=False)
    user_id = db.Column("user_id", db.Integer, ForeignKey("general.user.id"), nullable=False)

    def __init__(self, year_id, year_group_id, user_id):
        self.year_id = year_id
        self.group_id = year_group_id
        self.user_id = user_id


class RevueYear(db.Model):
    __tablename__ = "revue_year"
    __table_args__ = {"schema": "general"}
    id = db.Column("id", db.Integer, primary_key=True, nullable=False)
    title = db.Column("title", db.String(50), nullable=False)
    year = db.Column("year", db.Integer, nullable=False)

    def __init__(self, title, year):
        self.title = title
        self.year = year
