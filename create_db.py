from revue import db
from revue import models

db.create_all()

db.session.commit()