from flask import Blueprint, render_template

admin_site = Blueprint('admin', __name__, template_folder='../templates')

from revue.utilities.permissions import admin_required
from revue.admin.views import registration, user


@admin_site.before_request
@admin_required
def before_request():
    pass


@admin_site.route('/')
@admin_site.route('/home')
def index():
    return render_template("admin/index.html")
