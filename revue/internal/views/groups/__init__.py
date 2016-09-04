from flask import render_template, redirect, flash, url_for

import revue.utilities.group_pages as group_pages
import revue.utilities.groups as groups
import revue.utilities.menus as menus
from revue.internal.views import internal_site
from revue.models.groups import YearGroup, PersistentGroup
from revue.utilities.session import get_current_user


@internal_site.route('/group/<int:id>')
def show_group_by_id(id):
    return show_group(groups.get_group_by_id(id))


@internal_site.route('/group/<string:name>')
def show_group_by_name(name):
    return show_group(groups.get_group_by_name(name))


def show_group(group):
    if isinstance(group, PersistentGroup):
        return show_persistent_group(group)
    elif isinstance(group, YearGroup):
        return show_yeargroup(group)
    else:
        flash("Unknown group type", "danger")
        redirect("/")


def show_persistent_group(persistent_group):
    members = groups.get_persistent_group_members(persistent_group)
    menu_structure = menus.get_menu_structure(groups.get_group_menu(persistent_group))
    return render_template("internal/groups/persistent_group.html", group=persistent_group, members=members,
                           menu=menu_structure,
                           current_user_member=groups.get_persistent_group_participation(
                               persistent_group=persistent_group,
                               user=get_current_user()) is not None)


def show_yeargroup(year_group):
    members = groups.get_year_group_members_by_year(year_group)
    menu_structure = menus.get_menu_structure(groups.get_group_menu(year_group))
    years = sorted(members.keys())
    data_per_year = [{
                         "year": groups.get_revue_year_by_year(y),
                         "members": members[y],
                         "current_user_member": get_current_user() in members[y],
                         "user_requested_year_participation": groups.get_year_participation_request(
                             groups.get_revue_year_by_year(y), get_current_user()) is not None,
                         "user_member_of_year": groups.get_year_participation(groups.get_revue_year_by_year(y),
                                                                              get_current_user()) is not None
                     } for y in years]
    return render_template("internal/groups/year_group.html", group=year_group, data_per_year=data_per_year,
                           menu=menu_structure)


@internal_site.route('/year/current')
def show_current_year():
    return show_year(groups.get_current_year().year)


@internal_site.route('/year/<int:year>')
def show_year(year):
    revue_year = groups.get_revue_year_by_year(year)
    year_groups = groups.get_year_groups()
    return render_template("internal/groups/year.html", year=revue_year,
                           members=groups.get_revue_year_members(revue_year),
                           year_groups=year_groups,
                           user_is_member_of_year=groups.get_year_participation(revue_year,
                                                                                get_current_user()) is not None,
                           user_has_requested_year_participation=groups.get_year_participation_request(revue_year,
                                                                                                       get_current_user()) is not None)


@internal_site.route('/year/<int:year>/join')
def join_year(year):
    revue_year = groups.get_revue_year_by_year(year)
    groups.request_year_participation(revue_year, get_current_user())
    flash('Successfully asked to join year', 'success')
    return redirect(url_for('.index'))


@internal_site.route('/yeargroup/<int:id>')
def show_yeargroup_by_id(id):
    return show_yeargroup(groups.get_group_by_id(id))


@internal_site.route('/yeargroup/<int:year>/<int:id>')
def show_yeargroup_by_year_and_id(year, id):
    revue_year = groups.get_revue_year_by_year(year)
    year_group = groups.get_group_by_id(id)
    page = group_pages.get_or_create_year_group_year_page(year_group, revue_year)
    members = year_group.members(revue_year)
    return render_template("internal/groups/year_group_year.html", group=year_group, members=members, year=revue_year,
                           page=page,
                           current_user_member=get_current_user() in members,
                           is_year_participant=groups.get_year_participation(revue_year,
                                                                             get_current_user()) is not None,
                           has_requested_year_participation=groups.get_year_participation_request(revue_year,
                                                                                                  get_current_user()) is not None)


@internal_site.route('/yeargroup/<int:year>/<int:id>/join')
def join_yeargroup_by_year_and_id(year, id):
    revue_year = groups.get_revue_year_by_year(year)
    year_group = groups.get_group_by_id(id)
    groups.join_year_group(year_group=year_group, revue_year=revue_year, user=get_current_user())
    flash('Successfully joined group!', 'success')
    return redirect(url_for('.show_yeargroup_by_year_and_id', year=year, id=id))


@internal_site.route('/group/<int:id>/join')
def join_persistent_group_by_id(id):
    persistent_group = groups.get_group_by_id(id)
    groups.join_persistent_group(persistent_group=persistent_group, user=get_current_user())
    flash('Successfully joined group!', 'success')
    return redirect(url_for('.show_group_by_id', id=id))


@internal_site.route('/yeargroup/<int:year>/<int:id>/leave')
def leave_yeargroup_by_year_and_id(year, id):
    revue_year = groups.get_revue_year_by_year(year)
    year_group = groups.get_group_by_id(id)
    groups.leave_year_group(year_group, revue_year, get_current_user())
    flash('Successfully left group!', 'success')
    return redirect(url_for('.show_yeargroup_by_year_and_id', year=year, id=id))


@internal_site.route('/group/<int:id>/leave')
def leave_persistent_group_by_id(id):
    persistent_group = groups.get_group_by_id(id)
    groups.leave_persistent_group(persistent_group, get_current_user())
    flash('Successfully left group!', 'success')
    return redirect(url_for('.show_group_by_id', id=id))


@internal_site.route('/yeargroup/current/<int:id>')
def show_yeargroup_current_year(id):
    return show_yeargroup_by_year_and_id(2016, id)


@internal_site.route('/yeargroup/<int:year>/path')
def show_yeargroup_page_by_year(year, path):
    pass
