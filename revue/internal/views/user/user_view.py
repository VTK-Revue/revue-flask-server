__author__ = 'fkint'
from flask import render_template

from revue.models.general import User

from revue.utilities import session


def show(username):
    if username is None:
        user = session.get_current_user()
    else:
        user = User.query.filter_by(username=username).first()
    print("user = "+str(user))
    return render_template("internal/user/user.html", u=user)