#!/usr/bin/env python
# encoding: utf-8

from flask import Flask
import os


# Create application
app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])

from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.bcrypt import Bcrypt

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# Import blueprints
from revue.api import api
from revue.public.views import public_site
from revue.internal.views import internal_site

# Register blueprints
app.register_blueprint(api, url_prefix='/api')
app.register_blueprint(internal_site, url_prefix='/intern')
app.register_blueprint(public_site)

# Setup logging
# TODO: create sane defaults for development
import logging
logging.basicConfig(
    level=logging.DEBUG
)
