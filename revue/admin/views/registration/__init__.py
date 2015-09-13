from flask import render_template, flash, redirect, url_for

from revue.admin.views import admin_site
from revue.models.general import Registration, User
from revue import db


@admin_site.route("/registrations")
def registrations():
    return render_template("admin/registration/activate.html", registrations=Registration.query.all())


@admin_site.route("/registration/<username>/activate")
def activate_user(username):
    r = Registration.query.filter_by(username=username).first()
    if r is not None:
        u = User.from_registration(r)
        db.session.add(u)
        db.session.delete(r)
        db.session.commit()
        flash("Activated user " + str(username), "success")
    else:
        flash("No registration found for user " + str(username), "danger")
    return redirect(url_for('.registrations'))


@admin_site.route("/registration/<username>/remove")
def remove_registration(username):
    r = Registration.query.filter_by(username=username).first()
    if r is not None:
        db.session.delete(r)
        db.session.commit()
        flash("Removed registration for user " + str(username), "success")
    else:
        flash("No registration found for user " + str(username), "danger")
    return redirect(url_for('.registrations'))
