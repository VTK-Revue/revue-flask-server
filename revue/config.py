# http://flask.pocoo.org/docs/config/#development-production


class Config(object):
    # Run `python2 -c 'import os; print os.urandom(24)'`
    # to generate a random key
    # http://flask.pocoo.org/docs/0.10/quickstart/#sessions
    SECRET_KEY = ''
    DEBUG = False
    TESTING = False


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
