from flask import render_template, Blueprint

from revue.utilities.login import login_required
from revue.models.groups import Group, YearGroup

internal_site = Blueprint('intern', __name__, template_folder='../templates')


@internal_site.before_request
@login_required
def before_request():
    pass


from . import pages, groups, user


@internal_site.route("/")
@internal_site.route("/index")
def index():
    groups = Group.query.all()
    year_groups = YearGroup.query.all()
    for yg in year_groups:
        print(yg.id)
    return render_template("internal/index.html", groups=groups, year_groups=year_groups)


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
    return render_template("internal/members.html")
