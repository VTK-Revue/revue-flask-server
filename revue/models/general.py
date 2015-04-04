from revue import db, bcrypt

from sqlalchemy import ForeignKey, PrimaryKeyConstraint


class User(db.Model):
    __tablename__ = 'user'
    __table_args__ = {'schema': 'general'}
    id = db.Column('id', db.Integer, primary_key=True)
    firstName = db.Column(db.String(60))
    lastName = db.Column(db.String(60))
    email = db.Column(db.String(100))

    username = db.Column(db.String(20), unique=True)
    password = db.Column(db.String(60))

    def __init__(self, firstName, lastName, email, username, password):
        self.firstName = firstName
        self.lastName = lastName
        self.email = email

        self.username = username
        self.password = bcrypt.generate_password_hash(password)


class Registration(db.Model):
    __tablename__ = 'registration'
    __table_args__ = {'schema': 'general'}
    id = db.Column('id', db.Integer, primary_key=True)
    firstName = db.Column(db.String(60))
    lastName = db.Column(db.String(60))
    email = db.Column(db.String(100))

    username = db.Column(db.String(20), unique=True)
    password = db.Column(db.String(60))

    @classmethod
    def from_user(cls, u):
        return cls(u.firstName, u.lastName, u.email, u.username, u.password)

    def __init__(self, firstName, lastName, email, username, password):
        self.firstName = firstName
        self.lastName = lastName
        self.email = email

        self.username = username
        self.password = password


class Permission(db.Model):
    __tablename__ = "permission"
    __table_args__ = {"schema": "general"}
    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    def __init__(self, name):
        self.name = name


class UserPermission(db.Model):
    __tablename__ = "user_permission"
    __table_args__ = (PrimaryKeyConstraint("user", "permission"),{"schema":"general"})
    user = db.Column(db.Integer, ForeignKey('general.user.id'))
    permission = db.Column(db.Integer, ForeignKey('general.permission.id'))

    def __init__(self, user, permission):
        self.user = user
        self.permission = permission