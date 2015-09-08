from flask import render_template


def show_user(user):
    return render_template("internal/user/user.html", u=user)
