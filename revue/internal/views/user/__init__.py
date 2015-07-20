__author__ = 'fkint'
from flask import flash, redirect

from revue.internal.views import internal_site
from revue.utilities.login import login_required
from revue.utilities import session
import user_edit_view
import user_view


@internal_site.route("/user", methods=['GET'])
@login_required
def user_own():
    return user_edit_view.show()


@internal_site.route('/user', methods=['POST'])
@login_required
def update_user_data():
    return user_edit_view.show_update()


@internal_site.route("/user/<username>", methods=["GET"])
@login_required
def view_user(username):
    return user_view.show(username)


@internal_site.route("/logout")
@login_required
def logout():
    session.user_logout()
    flash('You just logged out', 'success')
    return redirect('/')
