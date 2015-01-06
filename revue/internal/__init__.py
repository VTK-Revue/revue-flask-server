from flask import Blueprint

internal_site = Blueprint('intern', __name__, template_folder='templates')

from . import views
