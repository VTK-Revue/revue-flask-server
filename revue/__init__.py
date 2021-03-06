#!/usr/bin/env python
# encoding: utf-8

import os
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_nav import Nav, register_renderer

# Create application
app = Flask(__name__)
mail = Mail(app)
Bootstrap(app)
nav = Nav()
app.config.from_object(os.environ['APP_SETTINGS'])

from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# Import blueprints
from revue.api import api
from revue.public.views import public_site
from revue.internal.views import internal_site
from revue.admin.views import admin_site

# Register blueprints
app.register_blueprint(api, url_prefix='/api')
app.register_blueprint(internal_site, url_prefix='/intern')
app.register_blueprint(admin_site, url_prefix='/admin')
app.register_blueprint(public_site)

# Setup logging
# TODO: create sane defaults for development
import logging

logging.basicConfig(
    level=logging.DEBUG
)

from revue.utilities.ui.bootstrap import CustomBootstrapRenderer

register_renderer(app, 'custom_bootstrap_nav', CustomBootstrapRenderer)
nav.init_app(app)

from revue.scripts import schedule_cron_jobs

schedule_cron_jobs()
