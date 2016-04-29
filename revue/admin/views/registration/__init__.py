from datetime import datetime

import os
from flask import render_template, flash, redirect, url_for
from flask_mail import Message

from revue import db
from revue import mail
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
        msg = Message("Account activated", sender="it@" + os.environ['EMAIL_SUFFIX'],
                      recipients=["it@" + os.environ['EMAIL_SUFFIX'], u.email().address])
        msg.body = ("Hi {},\n\n" +
                    "The IT team has activated your account. You can now sign in.\n\n" +
                    "Kind regards, \n\n The IT team").format(u.firstName)
        mail.send(msg)
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
