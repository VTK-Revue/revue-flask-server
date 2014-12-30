#!/usr/bin/env python
# encoding: utf-8

from flask import Flask

app = Flask(__name__)

from .api import api
from .public import public_site
from .internal import internal_site

# Setup logging
# TODO: create sane defaults for development
import logging
logging.basicConfig(
    level=logging.DEBUG
)
