from datetime import datetime

from flask import render_template, flash, redirect, url_for

from revue import db
from revue.admin.views import admin_site
from revue.models.general import User


@admin_site.route("/registrations")
def registrations():
    return render_template("admin/registration/activate.html", registrations=User.query.filter_by(activated=None).all())


@admin_site.route("/registration/<username>/activate")
def activate_user(username):
    u = User.query.filter_by(username=username, activated=None).first()
    if u is not None:
        u.activated = datetime.utcnow()
        db.session.commit()
        flash("Activated user " + str(username), "success")
    else:
        flash("No registration found for user " + str(username), "danger")
    return redirect(url_for('.registrations'))


@admin_site.route("/registration/<username>/remove")
def remove_registration(username):
    u = User.query.filter_by(username=username, activated=None).first()
    if u is not None:
        db.session.delete(u)
        db.session.commit()
        flash("Removed registration for user " + str(username), "success")
    else:
        flash("No registration found for user " + str(username), "danger")
    return redirect(url_for('.registrations'))
