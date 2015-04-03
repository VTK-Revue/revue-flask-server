__author__ = 'fkint'
from flask import render_template, session

from ....models.general import User


def show(username):
    if username is None:
        user = User.query.filter_by(id=session['logged_in_user_id']).first()
    else:
        user = User.query.filter_by(username=username).first()
    print("user = "+str(user))
    return render_template("internal/user/user.html", u=user)