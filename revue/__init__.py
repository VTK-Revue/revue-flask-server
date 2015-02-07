#!/usr/bin/env python
# encoding: utf-8

from flask import Flask


# Create application
app = Flask(__name__)
app.config.from_object('config.Config')

from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.bcrypt import Bcrypt

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# Import blueprints
from .api import api
from .public.views import public_site
from .internal.views import internal_site

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