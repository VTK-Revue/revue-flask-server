from flask import flash, redirect

from revue.internal.views import internal_site
from revue.utilities import session
from . import user_edit_view, user_view
from .groups import view_user_groups
from revue.models.general import User


@internal_site.route("/user/<int:id>", methods=["GET"])
def show_user(id):
    user = User.query.get(id)
    return user_view.show_user(user)


@internal_site.route("/user/<username>", methods=["GET"])
def view_user(username):
    if username is None:
        user = session.get_current_user()
    else:
        user = User.query.filter_by(username=username).first()
    return user_view.show_user(user)


@internal_site.route("/logout")
def logout():
    session.user_logout()
    flash('You just logged out', 'success')
    return redirect('/')


@internal_site.route("/user/groups", methods=["GET", "POST"])
def view_own_groups():
    user = session.get_current_user()
    return view_user_groups(user)


@internal_site.route("/user/<username>/groups", methods=["GET", "POST"])
def view_user_groups_by_username(username):
    user = User.query.filter_by(username=username).first()
    return view_user_groups(user)
