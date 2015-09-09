from revue.internal.views import internal_site
from revue.utilities.permissions import admin_required
from . import activate, user


@internal_site.route("/admin/user/<username>", methods=["GET"])
@admin_required
def show_admin_user(username=None):
    return user.show_user(username)


@internal_site.route("/admin/user/<username>", methods=["POST"])
@admin_required
def show_admin_user_update(username=None):
    return user.show_user_update(username)


@internal_site.route("/admin/activate")
@admin_required
def show_activate():
    return activate.show_activate_list()


@internal_site.route("/admin/activate/<username>")
@admin_required
def show_activate_user(username):
    return activate.show_activate_user(username)
