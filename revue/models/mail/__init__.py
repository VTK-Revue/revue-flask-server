import os
from sqlalchemy import ForeignKey

import revue.models.general
from revue import db
from revue.models.groups import PersistentGroup, YearGroup


class MailingAddress(db.Model):
    __tablename__ = 'address'
    __table_args__ = {'schema': 'mail'}
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50), nullable=True)
    __mapper_args__ = {
        'polymorphic_on': type
    }

    def get_address(self):
        raise Exception('get_address should be overridden')


class MailingAddressIntern(MailingAddress):
    __tablename__ = 'intern'
    __table_args__ = {'schema': 'mail'}
    __mapper_args__ = {
        'polymorphic_identity': "intern"
    }
    id = db.Column(db.Integer, db.ForeignKey('mail.address.id'), primary_key=True)
    name = db.Column(db.String(50), nullable=True, unique=True)

    def __init__(self, name):
        self.name = name

    def get_address(self):
        return self.name + "@" + os.environ['EMAIL_SUFFIX']

    def get_local_address(self):
        return self.name


class MailingList(MailingAddressIntern):
    __tablename__ = 'list'
    __table_args__ = {'schema': 'mail'}
    __mapper_args__ = {
        "polymorphic_identity": "list"
    }
    id = db.Column(db.Integer, db.ForeignKey('mail.intern.id'), primary_key=True)

    def members(self):
        return [e.get_address() for e in MailingListEntry.query.filter_by(list_id=self.id)]

    def __init__(self, name):
        MailingAddressIntern.__init__(self, name)


class PersistentGroupMailingList(MailingAddressIntern):
    __tablename__ = 'persistent_group_list'
    __table_args__ = {'schema': 'mail'}
    __mapper_args__ = {
        "polymorphic_identity": "persistent_group_list"
    }
    id = db.Column(db.Integer, db.ForeignKey('mail.intern.id'), primary_key=True)
    persistent_group_id = db.Column(db.Integer, db.ForeignKey('general.persistent_group.id'), nullable=False,
                                    unique=True)

    def __init__(self, persistent_group_id, name):
        MailingAddressIntern.__init__(self, name)
        self.persistent_group_id = persistent_group_id

    def members(self):
        pg = PersistentGroup.query.get(self.persistent_group_id)
        return [u.email() for u in pg.members()]


class YearGroupMailingList(MailingAddressIntern):
    __tablename__ = 'year_group_list'
    __table_args__ = {'schema': 'mail'}
    __mapper_args__ = {
        "polymorphic_identity": "year_group_list"
    }
    id = db.Column(db.Integer, db.ForeignKey('mail.intern.id'), primary_key=True)
    year_group_id = db.Column(db.Integer, db.ForeignKey('general.year_group.id'), primary_key=True, unique=True)

    def __init__(self, year_group_id, name):
        MailingAddressIntern.__init__(self, name)
        self.year_group_id = year_group_id

    def members(self, revue_year):
        yg = YearGroup.query.get(self.year_group_id)
        return [u.email() for u in yg.members(revue_year)]

    def get_local_address_year(self, revue_year):
        return self.get_local_address() + revue_year.get_mail_affix()

    def get_members_per_year(self):
        result = []
        for y in revue.models.general.RevueYear.query.all():
            result.append({
                "year": y,
                "members": self.members(y)
            })
        return result


class MailingAlias(MailingAddressIntern):
    __tablename__ = 'alias'
    __table_args__ = {'schema': 'mail'}
    __mapper_args__ = {
        "polymorphic_identity": "alias"
    }
    id = db.Column(db.Integer, db.ForeignKey('mail.intern.id'), primary_key=True)
    other_address_id = db.Column(db.Integer, db.ForeignKey('mail.address.id'), nullable=True)

    def other_address(self):
        return MailingAddress.query.get(self.other_address_id)


class MailingAddressLocal(MailingAddress):
    # TODO: let inherit from Internal!
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

    def __init__(self, address):
        MailingAddress.__init__(self)
        self.address = address

    def get_address(self):
        return self.address


class MailingListEntry(db.Model):
    __tablename__ = 'list_entry'
    __table_args__ = {'schema': 'mail'}
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    list_id = db.Column(db.Integer, ForeignKey('mail.list.id'), nullable=False)
    address_id = db.Column(db.Integer, ForeignKey('mail.address.id'), nullable=False)

    def get_address(self):
        return MailingAddress.query.get(self.address_id)

    def __init__(self, list_id, address_id):
        db.Model.__init__(self)
        self.list_id = list_id
        self.address_id = address_id