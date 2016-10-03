from datetime import datetime

import os
from flask import render_template, flash, redirect, url_for
from flask_mail import Message

from revue import db
from revue.utilities import groups
from revue import mail
from revue.admin.views import admin_site
from revue.models.general import User, RevueYear
from revue.models.groups import Group, YearParticipation, \
    SensitiveYearGroupParticipationRequest, SensitivePersistentGroupParticipationRequest


@admin_site.route("/registrations")
def registrations():
    registrations = User.query.filter_by(activated=None).all()

    persistent_group_join_requests = [(User.query.get(request.user_id), Group.query.get(request.group_id))
            for request in groups.get_sensitive_persistent_group_participation_requests()]

    year_group_join_requests = []
    for request in groups.get_sensitive_year_group_participation_requests():
        year_participation = YearParticipation.query.get(request.year_participation_id)
        year_group_join_requests.append((User.query.get(year_participation.user_id),
            Group.query.get(request.year_group_id),
            RevueYear.query.get(year_participation.year_id)))

    return render_template("admin/registration/activate.html",
            registrations=registrations,
            persistent_group_join_requests=persistent_group_join_requests,
            year_group_join_requests=year_group_join_requests)


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


@admin_site.route("/registration/persistent_group_request/<int:user_id>/<int:group_id>/approve")
def approve_sensitive_persistent_group_participation_request(user_id, group_id):
    user = User.query.filter_by(id=user_id).first()
    group = Group.query.filter_by(id=group_id).first()
    groups.approve_sensitive_persistent_group_participation_request(user, group)
    flash('User {} is now a member of persistent group {}'.format(user.username, group.name), 'success')
    return redirect(url_for('.registrations'))


@admin_site.route("/registration/persistent_group_request/<int:user_id>/<int:group_id>/reject")
def reject_sensitive_persistent_group_participation_request(user_id, group_id):
    user = User.query.filter_by(id=user_id).first()
    group = Group.query.filter_by(id=group_id).first()
    request = SensitivePersistentGroupParticipationRequest(user.id, group.id)
    db.session.delete(request)
    db.session.commit()
    flash('Participation request from user {} for persistent group {} rejected'
            .format(user.username, group.name), 'danger')
    return redirect(url_for('.registrations'))


@admin_site.route("/registration/year_group_request/<int:user_id>/<int:revue_year_id>/<int:group_id>/approve")
def approve_sensitive_year_group_participation_request(user_id, revue_year_id, group_id):
    user = User.query.get(user_id)
    revue_year = Group.query.get(revue_year_id)
    group = Group.query.get(group_id)

    groups.approve_sensitive_year_group_participation_request(user, revue_year, group)

    flash('User {} is now a member of year group {} ({})'.format(user.username, group.name, revue_year.year), 'success')
    return redirect(url_for('.registrations'))


@admin_site.route("/registration/year_group_request/<int:user_id>/<int:revue_year_id>/<int:group_id>/reject")
def reject_sensitive_year_group_participation_request(user_id, revue_year_id, group_id):
    user = User.query.get(user_id)
    revue_year = RevueYear.query.get(revue_year_id)
    group = Group.query.get(group_id)

    year_participation = groups.get_year_participation(revue_year=revue_year, user=user)
    request = SensitiveYearGroupParticipationRequest(year_group_id=group.id, year_participation_id=year_participation.id)
    db.session.delete(request)
    db.session.commit()

    flash('Participation request from user {} for year group {} ({}) rejected'.format(user.username, group.name, revue_year.year), 'danger')
    return redirect(url_for('.registrations'))
