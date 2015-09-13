from flask import render_template

from revue.utilities import groups


def view_user_groups(user):
    general_groups = groups.get_user_persistent_groups(user)
    year_groups_by_year = groups.get_user_year_groups_by_year(user)
    return render_template("internal/user/user_groups.html", user=user, general_groups=general_groups,
                           year_groups_by_year=year_groups_by_year)
