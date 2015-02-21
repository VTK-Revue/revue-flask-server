__author__ = 'fkint'
from flask import render_template

from ...models.general import User


def show(username):
    user = User.query.filter_by(username=username).first()
    print(user)
    return render_template("internal/user.html", u=user)