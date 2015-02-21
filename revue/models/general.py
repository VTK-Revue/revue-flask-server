from revue import db, bcrypt

from sqlalchemy import func

class User(db.Model):
    __tablename__ = 'user'
    __table_args__ = {'schema': 'general'}
    id = db.Column('id', db.Integer, primary_key=True)
    firstName = db.Column(db.String(60))
    lastName = db.Column(db.String(60))
    email = db.Column(db.String(50))

    username = db.Column(db.String(20), unique=True)
    password = db.Column(db.String())

    def __init__(self, firstName, lastName, email, username, password):
        self.firstName = firstName
        self.lastName = lastName
        self.email = email

        self.username = username
        self.password = bcrypt.generate_password_hash(password)
