from flask import Blueprint

api = Blueprint('api', __name__)

# views.py defines API endpoints
from . import views
