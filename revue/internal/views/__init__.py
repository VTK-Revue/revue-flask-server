from flask import render_template, Blueprint

from revue.utilities.login import login_required

internal_site = Blueprint('intern', __name__, template_folder='../templates')

import pages
import groups
import user
import admin


@internal_site.route("/")
@internal_site.route("/index")
@login_required
def index():
    return render_template("internal/index.html")


@internal_site.route("/script")
@login_required
def script():
    return render_template("internal/script.html")


@internal_site.route("/activities")
@login_required
def activities():
    return render_template("internal/activities.html")

@internal_site.route("/media")
@login_required
def media():
    return render_template("internal/media.html")

@internal_site.route("/members")
@login_required
def members():
    return render_template("internal/members.html")