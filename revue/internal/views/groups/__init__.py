__author__ = 'Floris'

from revue.internal.views import internal_site
from revue.utilities.login import  login_required
import revue.utilities.groups as groups
from revue.models import Group, YearGroup, YearGroupParticipation, RevueYear, User
from flask import render_template


@internal_site.route('/group/<int:id>')
@login_required
def show_group_by_id(id):
    return show_group(Group.query.get(id))


@internal_site.route('/group/<string:name>')
@login_required
def show_group_by_name(name):
    return show_group(Group.query.filter_by(name=name).first())


def show_group(group):
    members = groups.get_group_members(group)
    return render_template("internal/groups/group.html", group=group, members=members)


@internal_site.route('/yeargroup/<int:id>')
@login_required
def show_yeargroup_by_id(id):
    return show_group(YearGroup.query.get(id))

@internal_site.route('/yeargroup/<int:year>/<int:id>')
@login_required
def show_yeargroup_by_year_and_id(year, id):
    revue_year = RevueYear.query.filter_by(year=year).first()
    participations = YearGroupParticipation.query.filter_by(year=revue_year.id, year_group=id)
    members = [User.query.get(p.user) for p in participations]
    year_group = YearGroup.query.get(id)
    return render_template("internal/groups/year_group_year.html", group=year_group, members=members)

@internal_site.route('/yeargroup/<int:year>/path')
@login_required
def show_yeargroup_page_by_year(year, path):
    pass