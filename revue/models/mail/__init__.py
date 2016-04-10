from sqlalchemy import ForeignKey

from revue import db


class MailingAddress(db.Model):
    __tablename__ = 'address'
    __table_args__ = {'schema': 'mail'}
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50), nullable=True)
    __mapper_args__ = {
        'polymorphic_on': type
    }


class MailingAddressIntern(MailingAddress):
    __tablename__ = 'intern'
    __table_args__ = {'schema': 'mail'}
    __mapper_args__ = {
        'polymorphic_identity': "intern"
    }
    id = db.Column(db.Integer, db.ForeignKey('mail.address.id'), primary_key=True)
    name = db.Column(db.String(50), nullable=True, unique=True)


class MailingList(MailingAddressIntern):
    __tablename__ = 'list'
    __table_args__ = {'schema': 'mail'}
    __mapper_args__ = {
        "polymorphic_identity": "list"
    }
    id = db.Column(db.Integer, db.ForeignKey('mail.intern.id'), primary_key=True)


class PersistentGroupMailingList(MailingList):
    __tablename__ = 'persistent_group_list'
    __table_args__ = {'schema': 'mail'}
    __mapper_args__ = {
        "polymorphic_identity": "persistent_group_list"
    }
    id = db.Column(db.Integer, db.ForeignKey('mail.list.id'), primary_key=True)
    persistent_group_id = db.Column(db.Integer, db.ForeignKey('general.persistent_group.id'), nullable=False, unique=True)


class YearGroupMailingList(MailingList):
    __tablename__ = 'year_group_list'
    __table_args__ = {'schema': 'mail'}
    __mapper_args__ = {
        "polymorphic_identity": "year_group_list"
    }
    id = db.Column(db.Integer, db.ForeignKey('mail.list.id'), primary_key=True)
    year_group_id = db.Column(db.Integer, db.ForeignKey('general.year_group.id'), primary_key=True, unique=True)


class MailingAlias(MailingAddressIntern):
    __tablename__ = 'alias'
    __table_args__ = {'schema': 'mail'}
    __mapper_args__ = {
        "polymorphic_identity": "alias"
    }
    id = db.Column(db.Integer, db.ForeignKey('mail.intern.id'), primary_key=True)
    other_address_id = db.Column(db.Integer, db.ForeignKey('mail.address.id'), nullable=True)


class MailingAddressLocal(MailingAddress):
    __tablename__ = 'local_address'
    __table_args__ = {'schema': 'mail'}
    __mapper_args__ = {
        "polymorphic_identity": "local"
    }
    id = db.Column(db.Integer, db.ForeignKey('mail.address.id'), primary_key=True)


class MailingAddressExtern(MailingAddress):
    __tablename__ = 'extern_address'
    __table_args__ = {'schema': 'mail'}
    __mapper_args__ = {
        "polymorphic_identity": "extern"
    }
    id = db.Column(db.Integer, db.ForeignKey('mail.address.id'), primary_key=True)
    address = db.Column(db.String(150), nullable=False)


class MailingListEntry(db.Model):
    __tablename__ = 'list_entry'
    __table_args__ = {'schema': 'mail'}
    id = db.Column(db.Integer, primary_key=True)
    list_id = db.Column(db.Integer, ForeignKey('mail.list.id'), nullable=False)
    address_id = db.Column(db.Integer, ForeignKey('mail.address.id'), nullable=False)
    type = db.Column(db.String(50), nullable=True)
    __mapper_args__ = {
        'polymorphic_on': type
    }