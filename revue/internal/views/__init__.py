from flask import render_template, Blueprint
from revue.utilities.login import login_required



internal_site = Blueprint('intern', __name__, template_folder='../templates')


from user import user_view
from user import user_edit_view

@internal_site.route("/")
@internal_site.route("/index")
@login_required
def index():
    return render_template("internal/index.html")


@internal_site.route("/script")
@login_required
def script():
    return render_template("internal/script.html")


@internal_site.route("/activities")
@login_required
def activities():
    return render_template("internal/activities.html")

@internal_site.route("/user",methods=['GET'])
@login_required
def user_own():
    return user_edit_view.show()


@internal_site.route('/user',methods=['POST'])
@login_required
def update_user_data():
    return user_edit_view.show_update()


@internal_site.route("/user/<username>", methods=["GET"])
@login_required
def user(username):
    return user_view.show(username)



import admin.user as admin_user
import admin.activate as admin_activate

from revue.utilities.permissions import admin_required

@internal_site.route("/admin/user/<username>", methods=["GET"])
@admin_required
def show_admin_user(username=None):
    return admin_user.show_user(username)

@internal_site.route("/admin/user/<username>", methods=["POST"])
@admin_required
def show_admin_user_update(username=None):
    return admin_user.show_user_update(username)

@internal_site.route("/admin/activate")
@admin_required
def show_activate():
    return admin_activate.show_activate_list()

@internal_site.route("/admin/activate/<username>")
@admin_required
def show_activate_user(username):
    return admin_activate.show_activate_user(username)

import pages

