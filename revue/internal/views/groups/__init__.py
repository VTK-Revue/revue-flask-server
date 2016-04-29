from flask import render_template, redirect, flash, url_for

import revue.utilities.groups as groups
import revue.utilities.menus as menus
from revue import db
from revue.internal.views import internal_site
from revue.models.general import User, RevueYear
from revue.models.groups import Group, YearGroup, YearGroupParticipation, PersistentGroupParticipation
from revue.utilities.session import get_current_user_id, get_current_user


@internal_site.route('/group/<int:id>')
def show_group_by_id(id):
    return show_group(Group.query.get(id))


@internal_site.route('/group/<string:name>')
def show_group_by_name(name):
    return show_group(Group.query.filter_by(name=name).first())


def show_group(group):
    members = groups.get_group_members(group)
    menu_structure = menus.get_menu_structure(groups.get_group_menu(group))
    return render_template("internal/groups/group.html", group=group, members=members, menu=menu_structure,
                           current_user_member=groups.is_user_member_of_persistent_group(group_id=group.id,
                                                                                         user_id=get_current_user_id()))


def show_yeargroup(yeargroup):
    members = groups.get_year_group_members_by_year(yeargroup.id)
    menu_structure = menus.get_menu_structure(groups.get_group_menu(yeargroup))
    years = sorted(members.keys())
    data_per_year = [
        {
            "year": RevueYear.query.filter_by(year=y).first(),
            "members": members[y],
            "current_user_member": get_current_user() in members[y]
        }
        for y in years
        ]
    return render_template("internal/groups/year_group.html", group=yeargroup, data_per_year=data_per_year,
                           menu=menu_structure)


@internal_site.route('/yeargroup/<int:id>')
def show_yeargroup_by_id(id):
    return show_yeargroup(YearGroup.query.get(id))


@internal_site.route('/yeargroup/<int:year>/<int:id>')
def show_yeargroup_by_year_and_id(year, id):
    revue_year = RevueYear.query.filter_by(year=year).first()
    participations = YearGroupParticipation.query.filter_by(year_id=revue_year.id, group_id=id)
    members = [User.query.get(p.user_id) for p in participations]
    year_group = YearGroup.query.get(id)
    return render_template("internal/groups/year_group_year.html", group=year_group, members=members, year=revue_year,
                           current_user_member=get_current_user() in members)


@internal_site.route('/yeargroup/<int:year>/<int:id>/join')
def join_yeargroup_by_year_and_id(year, id):
    revue_year = RevueYear.query.filter_by(year=year).first()
    if YearGroupParticipation.query.filter_by(year_id=revue_year.id, group_id=id,
                                              user_id=get_current_user_id()).count():
        flash('Already member of this group!', 'warning')
    else:
        p = YearGroupParticipation(revue_year.id, id, get_current_user_id())
        db.session.add(p)
        db.session.commit()
        flash('Successfully joined year group', 'success')
    return redirect(url_for('.show_yeargroup_by_year_and_id', year=year, id=id))


@internal_site.route('/group/<int:id>/join')
def join_persistent_group_by_id(id):
    if PersistentGroupParticipation.query.filter_by(group_id=id, user_id=get_current_user_id()).count():
        flash('Already member of this group!', 'warning')
    else:
        p = PersistentGroupParticipation(id, get_current_user_id())
        db.session.add(p)
        db.session.commit()
        flash('Successfully joined group!', 'success')
    return redirect(url_for('.show_group_by_id', id=id))


@internal_site.route('/yeargroup/<int:year>/<int:id>/leave')
def leave_yeargroup_by_year_and_id(year, id):
    revue_year = RevueYear.query.filter_by(year=year).first()
    p = YearGroupParticipation.query.filter_by(year_id=revue_year.id, group_id=id,
                                               user_id=get_current_user_id()).first()
    db.session.delete(p)
    db.session.commit()
    flash('Successfully left group!', 'success')
    return redirect(url_for('.show_yeargroup_by_year_and_id', year=year, id=id))


@internal_site.route('/group/<int:id>/leave')
def leave_persistent_group_by_id(id):
    p = PersistentGroupParticipation.query.filter_by(group_id=id, user_id=get_current_user_id()).first()
    db.session.delete(p)
    db.session.commit()
    flash('Successfully left group!', 'success')
    return redirect(url_for('.show_group_by_id', id=id))


@internal_site.route('/yeargroup/current/<int:id>')
def show_yeargroup_current_year(id):
    return show_yeargroup_by_year_and_id(2016, id)


@internal_site.route('/yeargroup/<int:year>/path')
def show_yeargroup_page_by_year(year, path):
    pass
