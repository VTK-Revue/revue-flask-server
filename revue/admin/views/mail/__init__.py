from flask import render_template

from revue.admin.views import admin_site
from revue.models.mail import PersistentGroupMailingList, YearGroupMailingList


@admin_site.route('/mail/persistent_group/<int:persistent_group_id>')
def view_persistent_group_mailing_list(persistent_group_id):
    l = PersistentGroupMailingList.query.filter_by(persistent_group_id=persistent_group_id).one()
    return render_template('admin/mail/mailing_list.html', members=l.members())


@admin_site.route('/mail/year_gruop/<int:year_group_id>')
def view_year_group_mailing_list(year_group_id):
    l = YearGroupMailingList.query.filter_by(year_group_id=year_group_id).one()
    return render_template('admin/mail/year_group_mailing_list.html', members=l.get_members_per_year())
