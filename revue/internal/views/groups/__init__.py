from flask import render_template

from revue.internal.views import internal_site
import revue.utilities.groups as groups
import revue.utilities.menus as menus
from revue.models.groups import Group, YearGroup, YearGroupParticipation, RevueYear
from revue.models.general import User


@internal_site.route('/group/<int:id>')
def show_group_by_id(id):
    return show_group(Group.query.get(id))


@internal_site.route('/group/<string:name>')
def show_group_by_name(name):
    return show_group(Group.query.filter_by(name=name).first())


def show_group(group):
    members = groups.get_group_members(group)
    menu_structure = menus.get_menu_structure(groups.get_group_menu(group))
    return render_template("internal/groups/group.html", group=group, members=members, menu=menu_structure)


@internal_site.route('/yeargroup/<int:id>')
def show_yeargroup_by_id(id):
    return show_group(YearGroup.query.get(id))


@internal_site.route('/yeargroup/<int:year>/<int:id>')
def show_yeargroup_by_year_and_id(year, id):
    revue_year = RevueYear.query.filter_by(year=year).first()
    participations = YearGroupParticipation.query.filter_by(year=revue_year.id, year_group=id)
    members = [User.query.get(p.user) for p in participations]
    year_group = YearGroup.query.get(id)
    return render_template("internal/groups/year_group_year.html", group=year_group, members=members, year=revue_year)


@internal_site.route('/yeargroup/current/<int:id>')
def show_yeargroup_current_year(id):
    return show_yeargroup_by_year_and_id(2015, id)


@internal_site.route('/yeargroup/<int:year>/path')
def show_yeargroup_page_by_year(year, path):
    pass
