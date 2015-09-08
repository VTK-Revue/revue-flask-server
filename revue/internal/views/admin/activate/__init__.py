from flask import render_template, flash, request

from revue.models import Registration, User
from revue import db


def show_activate_list():
    registrations = Registration.query.all();
    activate_url = lambda username: "/intern/admin/activate/" + username + "?ok=1"
    remove_registration_url = lambda username: "/intern/admin/activate/" + username + "?ok=0"
    return render_template("internal/admin/activate.html", registrations=registrations, activate_url=activate_url,
                           remove_registration_url=remove_registration_url)


def show_activate_user(username):
    ok = str(request.args.get("ok", 0)) == "1"
    r = Registration.query.filter_by(username=username).first()
    if r is not None:
        if ok:
            u = User.from_registration(r)
            db.session.add(u)
            db.session.delete(r)
            db.session.commit()
            flash("Activated user " + str(username))
        else:
            db.session.delete(r)
            db.session.commit()
            flash("Removed registration for user " + str(username))
    else:
        flash("No registration found for user " + str(username))
    return show_activate_list()
