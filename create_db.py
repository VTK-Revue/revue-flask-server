from revue import db
from revue import models

print "create"

db.create_all()

db.session.commit()