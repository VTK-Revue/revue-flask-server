from sqlalchemy import ForeignKey, PrimaryKeyConstraint
from sqlalchemy.orm import relationship

from revue import db, bcrypt
from revue.models.mail import MailingAddressExtern

class User(db.Model):
    __tablename__ = 'user'
    __table_args__ = {'schema': 'general'}
    id = db.Column('id', db.Integer, primary_key=True)
    firstName = db.Column(db.String(60))
    lastName = db.Column(db.String(60))
    email_address_id = db.Column(db.Integer, ForeignKey('mail.extern_address.id'))

    username = db.Column(db.String(20), unique=True)
    password = db.Column(db.String(60))

    activated = db.Column(db.DateTime, default=None, nullable=True)

    content_elements = relationship("ContentElement", backref="author")

    def __init__(self, firstName, lastName, email_address_id, username, password=None, activated=None):
        self.firstName = firstName
        self.lastName = lastName
        self.email_address_id = email_address_id

        self.username = username
        if password is None:
            self.password = None
        else:
            self.password = bcrypt.generate_password_hash(password).decode("utf-8")
        self.activated = activated

    def email(self):
        return MailingAddressExtern.query.get(self.email_address_id)

    def name(self):
        return self.firstName + " " + self.lastName

    @classmethod
    def from_registration(cls, r):
        u = cls(r.firstName, r.lastName, r.email, r.username)
        u.password = r.password
        return u


class Permission(db.Model):
    __tablename__ = "permission"
    __table_args__ = {"schema": "general"}
    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column(db.String(50))

    def __init__(self, name):
        self.name = name


class UserPermission(db.Model):
    __tablename__ = "user_permission"
    __table_args__ = (PrimaryKeyConstraint("user_id", "permission_id"), {"schema": "general"})
    user_id = db.Column(db.Integer, ForeignKey('general.user.id'))
    permission_id = db.Column(db.Integer, ForeignKey('general.permission.id'))

    def __init__(self, user_id, permission_id):
        self.user_id = user_id
        self.permission_id = permission_id
