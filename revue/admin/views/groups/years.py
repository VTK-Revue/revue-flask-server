import os
from flask import flash
from flask import render_template
from flask_mail import Message

from revue import mail
from revue.admin.views import admin_site
from revue.models.general import User
from revue.utilities import groups


@admin_site.route('/years')
def show_all_years():
    return render_template('admin/groups/years.html', years=groups.get_all_revue_years())


@admin_site.route('/year/<int:year>/participations')
def show_year_participations(year):
    revue_year = groups.get_revue_year_by_year(year)
    participations = groups.get_year_participations(revue_year)
    pending_requests = groups.get_pending_year_participation_requests(revue_year)
    return render_template('admin/groups/year_participations.html', year=revue_year, participations=participations,
                           pending_requests=pending_requests)


@admin_site.route('/year/<int:year>/request/<int:user>/approve')
def approve_year_participation_request(year, user):
    user = User.query.get(user)
    revue_year = groups.get_revue_year_by_year(year)
    groups.approve_year_participation_request(user, revue_year)
    flash('Request approved', 'success')
    msg = Message("Your Revue year participation request was approved", sender="it@" + os.environ['EMAIL_SUFFIX'],
                  recipients=["it@" + os.environ['EMAIL_SUFFIX'], user.email().get_address()])
    msg.body = ("Hi {}\n\n" +
                "Your request to join the Revue year {} was approved. " +
                "You can now join working groups for that year.." +
                "\n\nKind regards,\n\nRevue IT").format(user.name(), revue_year.year)
    mail.send(msg)
    return show_year_participations(year)


@admin_site.route('/year/<int:year>/request/<int:user>/reject')
def reject_year_participation_request(year, user):
    user = User.query.get(user)
    revue_year = groups.get_revue_year_by_year(year)
    groups.reject_year_participation_request(user, revue_year)
    flash('Participation request rejected.', 'success')
    return show_year_participations(year)
