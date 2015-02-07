# http://flask.pocoo.org/docs/config/#development-production

import os


class Config(object):
    # Run `python2 -c 'import os; print os.urandom(24)'`
    # to generate a random key
    # http://flask.pocoo.org/docs/0.10/quickstart/#sessions
    SECRET_KEY = 'Some key'
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = "postgresql://revue:revuedb@localhost/revue"


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
