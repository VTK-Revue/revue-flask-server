from flask import render_template, Blueprint

from revue.models.groups import Group, YearGroup
from revue.utilities import users
from revue.utilities.login import login_required

internal_site = Blueprint('intern', __name__, template_folder='../templates')


@internal_site.before_request
@login_required
def before_request():
    pass


from . import pages, groups, user, upload


@internal_site.route("/")
@internal_site.route("/index")
def index():
    gs = Group.query.all()
    year_groups = YearGroup.query.all()
    return render_template("internal/index.html", groups=gs, year_groups=year_groups)


@internal_site.route("/script")
def script():
    return render_template("internal/script.html")


@internal_site.route("/activities")
def activities():
    return render_template("internal/activities.html")


@internal_site.route("/media")
def media():
    return render_template("internal/media.html")


@internal_site.route("/members")
def members():
    return render_template("internal/members.html", users=users.get_all_users())
