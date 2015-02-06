#!/usr/bin/env python
# encoding: utf-8

from flask import Flask

# Create application
app = Flask(__name__)
app.config.from_object('config.Config')

# Import database handlers
from flask.ext.sqlalchemy import SQLAlchemy

# Database setup
db = SQLAlchemy(app)

# Import blueprints
from .api import api
from .public import public_site
from .internal import internal_site

# Register blueprints
app.register_blueprint(api, url_prefix='/api')
app.register_blueprint(public_site)
app.register_blueprint(internal_site, url_prefix='/intern')

# Setup logging
# TODO: create sane defaults for development
import logging
logging.basicConfig(
    level=logging.DEBUG
)