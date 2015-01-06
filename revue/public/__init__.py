from flask import Blueprint

public_site = Blueprint('public', __name__, template_folder='templates')

from . import views
