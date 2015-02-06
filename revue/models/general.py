from revue import db

class User(db.Model):
	__tablename__ = 'user'
	__table_args__ = {'schema': 'general'}
	id = db.Column('id', db.Integer, primary_key = True)
	firstName = db.Column(db.String(60))
	lastName = db.Column(db.String(60))

	def __init__(self, firstName, lastName):
		self.firstName = firstName
		self.lastName = lastName