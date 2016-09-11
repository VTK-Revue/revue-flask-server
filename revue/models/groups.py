import revue.models.general
import revue.models.mail
from revue import db


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
    persistent_group_id = db.Column("id", db.Integer, db.ForeignKey('general.group.id'), primary_key=True, nullable=False)
    parent_persistent_group_id = db.Column(db.Integer, db.ForeignKey("general.persistent_group.id"), nullable=True)
    listed = db.Column(db.Boolean, nullable=False, default=True)
    __mapper_args__ = {
        "polymorphic_identity": "persistent_group"
    }

    def mailing_list(self):
        return revue.models.mail.PersistentGroupMailingList.query.filter_by(
            persistent_group_id=self.persistent_group_id).one_or_none()

    def members(self):
        return [revue.models.general.User.query.get(pgp.user_id) for pgp in
                PersistentGroupParticipation.query.filter_by(group_id=self.id)]


class YearGroup(Group):
    __tablename__ = "year_group"
    __table_args__ = {"schema": "general"}
    year_group_id = db.Column("id", db.Integer, db.ForeignKey('general.group.id'), primary_key=True, nullable=False)
    parent_year_group_id = db.Column("parent_year_group_id", db.Integer, db.ForeignKey("general.year_group.id"),
                                     nullable=True)
    __mapper_args__ = {
        "polymorphic_identity": "year_group"
    }

    def mailing_list(self):
        return revue.models.mail.YearGroupMailingList.query.filter_by(
            year_group_id=self.year_group_id).one_or_none()

    def members(self, revue_year):
        year_participation_ids = [x.id for x in revue_year.participations()]
        year_group_participations = YearGroupParticipation.query.filter(
            db.and_(YearGroupParticipation.year_participation_id.in_(year_participation_ids),
                 YearGroupParticipation.year_group_id == self.id)).all()
        return [revue.models.general.User.query.get(ygp.year_participation().user_id) for ygp in
                year_group_participations]


class PersistentGroupParticipation(db.Model):
    __tablename__ = "persistent_group_participation"
    __table_args__ = (db.PrimaryKeyConstraint("persistent_group_id", "user_id"), {"schema": "general"})
    group_id = db.Column("persistent_group_id", db.Integer, db.ForeignKey("general.group.id"), nullable=False)
    user_id = db.Column("user_id", db.Integer, db.ForeignKey("general.user.id"), nullable=False)

    def __init__(self, persistent_group_id, user_id):
        self.group_id = persistent_group_id
        self.user_id = user_id


class YearParticipationRequest(db.Model):
    __tablename__ = "year_participation_request"
    __table_args__ = (db.UniqueConstraint('year_id', 'user_id'), {"schema": "general"})
    id = db.Column("id", db.Integer, primary_key=True, nullable=False)
    year_id = db.Column("year_id", db.Integer, db.ForeignKey("general.revue_year.id"), nullable=False)
    user_id = db.Column("user_id", db.Integer, db.ForeignKey("general.user.id"), nullable=False)

    def __init__(self, year_id, user_id):
        self.year_id = year_id
        self.user_id = user_id

    def user(self):
        return revue.models.general.User.query.get(self.user_id)


class YearParticipation(YearParticipationRequest):
    __tablename__ = "year_participation"
    __table_args__ = {"schema": "general"}
    participation_id = db.Column("id", db.Integer, db.ForeignKey("general.year_participation_request.id"), nullable=False,
                                 primary_key=True)


class YearGroupParticipation(db.Model):
    __tablename__ = "year_group_participation"
    __table_args__ = (db.PrimaryKeyConstraint("year_group_id", "year_participation_id"), {"schema": "general"})
    year_group_id = db.Column("year_group_id", db.Integer, db.ForeignKey("general.year_group.id"), nullable=False)
    year_participation_id = db.Column("year_participation_id", db.Integer, db.ForeignKey("general.year_participation.id"),
                                      nullable=False)

    def __init__(self, year_participation_id, year_group_id):
        self.year_participation_id = year_participation_id
        self.year_group_id = year_group_id

    def year_participation(self):
        return YearParticipation.query.get(self.year_participation_id)
