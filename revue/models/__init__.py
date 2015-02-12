# Import database handlers
from revue import app, db
from sqlalchemy import create_engine
from sqlalchemy.schema import CreateSchema

engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])

# Try create general scheme and load all general models
try:
    engine.execute(CreateSchema('general'))
except Exception:
    pass

from general import *
