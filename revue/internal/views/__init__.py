from flask import render_template, Blueprint, request
from revue.login import login_required

from user import user_view
from user import user_edit_view


internal_site = Blueprint('intern', __name__, template_folder='../templates')


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


@internal_site.route("/user/<username>")
@login_required
def user(username=None):
    return user_view.show(username)


@internal_site.route("/admin/user")
@login_required
def admin_user():
    return render_template("internal/admin/user.html")
