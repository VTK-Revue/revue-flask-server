from flask import flash, redirect

from revue.internal.views import internal_site
from revue.utilities.login import login_required
from revue.utilities import session
import user_edit_view
import user_view
from .groups import view_user_groups
from revue.models import User


@internal_site.route("/user", methods=['GET'])
@login_required
def user_own():
    return user_edit_view.show()


@internal_site.route('/user', methods=['POST'])
@login_required
def update_user_data():
    return user_edit_view.show_update()


@internal_site.route("/user/<int:id>", methods=["GET"])
@login_required
def show_user(id):
    user = User.query.get(id)
    return user_view.show_user(user)


@internal_site.route("/user/<username>", methods=["GET"])
@login_required
def view_user(username):
    if username is None:
        user = session.get_current_user()
    else:
        user = User.query.filter_by(username=username).first()
    return user_view.show_user(user)


@internal_site.route("/logout")
@login_required
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
