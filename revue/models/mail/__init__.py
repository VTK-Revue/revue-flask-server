from sqlalchemy import ForeignKey

from revue import db


# TODO: do id fields need to be copied when inheriting?

class MailingAddress(db.Model):
    __tablename__ = 'address'
    __table_args__ = {'schema': 'mail'}
    id = db.Column('id', db.Integer, primary_key=True)
    type = db.Column(db.String(50), nullable=True)
    __mapper_args__ = {
        'polymorphic_on': type
    }


class MailingList(MailingAddress):
    __tablename__ = 'list'
    __table_args__ = {'schema': 'mail'}
    __mapper_args__ = {
        "polymorphic_identity": "list"
    }


class MailingAlias(MailingAddress):
    __tablename__ = 'alias'
    __table_args__ = {'schema': 'mail'}
    __mapper_args__ = {
        "polymorphic_identity": "alias"
    }


class MailingAddressLocal(MailingAddress):
    __tablename__ = 'local_address'
    __table_args__ = {'schema': 'mail'}
    __mapper_args__ = {
        "polymorphic_identity": "local"
    }


class MailingAddressExtern(MailingAddress):
    __tablename__ = 'extern_address'
    __table_args__ = {'schema': 'mail'}
    __mapper_args__ = {
        "polymorphic_identity": "extern"
    }


class MailingListEntry(db.Model):
    __tablename__ = 'list_entry'
    __table_args__ = {'schema': 'mail'}
    id = db.Column('id', db.Integer, primary_key=True)
    list_id = db.Column('list_id', db.Integer, ForeignKey('mail.list.id'), nullable=False)
    address_id = db.Column('address_id', db.Integer, ForeignKey('mail.address.id'), nullable=False)
    type = db.Column(db.String(50), nullable=True)
    __mapper_args__ = {
        'polymorphic_on': type
    }


class PersistentGroupMailingListEntry(MailingListEntry):
    group_id = db.Column('group_id', db.Integer, ForeignKey('general.persistent_group.id'), nullable=False)
    __mapper_args__ = {
        "polymorphic_identity": "persistent_group"
    }


class YearGroupYearMailingListEntry(MailingListEntry):
    year_group_id = db.Column('year_group_id', db.Integer, ForeignKey('general.persistent_group.persistent_group_id'),
                              nullable=False)
    year_id = db.Column('year_id', db.Integer, ForeignKey('general.revue_year.id'), nullable=False)
    __mapper_args__ = {
        "polymorphic_identity": "year_group"
    }
