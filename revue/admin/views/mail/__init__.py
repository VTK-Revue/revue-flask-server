from flask import flash, request
from flask import render_template
from revue import db
from revue.admin.views import admin_site
from revue.admin.views.mail.forms import AddMailingListEntryForm, CreateMailingListForm
from revue.models.mail import PersistentGroupMailingList, YearGroupMailingList, MailingList, MailingListEntry, MailingAddressExtern
from revue.scripts.mail import generate_all_mail_files


@admin_site.route('/mail/persistent_group/<int:persistent_group_id>')
def view_persistent_group_mailing_list(persistent_group_id):
    l = PersistentGroupMailingList.query.filter_by(persistent_group_id=persistent_group_id).one()
    return render_template('admin/mail/persistent_group_mailing_list.html', members=l.members())


@admin_site.route('/mail/year_group/<int:year_group_id>')
def view_year_group_mailing_list(year_group_id):
    l = YearGroupMailingList.query.filter_by(year_group_id=year_group_id).one()
    return render_template('admin/mail/year_group_mailing_list.html', members=l.get_members_per_year())


@admin_site.route('/mail/generate_lists')
def generate_mail_lists():
    generate_all_mail_files()
    flash('Mail files generated', 'success')
    return render_template('admin/mail/generate_lists.html')


@admin_site.route('/mail/lists', methods=['GET', 'POST'])
def view_mailing_lists():
    new_list_form = CreateMailingListForm(request.form)
    if new_list_form.validate_on_submit():
        lst = MailingList(new_list_form.name.data)
        db.session.add(lst)
        db.session.commit()
        flash('Successfully added a list', 'success')
    return render_template('admin/mail/mailing_lists.html', lists=MailingList.query.all(), new_list_form=new_list_form)


@admin_site.route('/mail/list/<int:list_id>', methods=['GET', 'POST'])
def view_mailing_list(list_id):
    lst = MailingList.query.get(list_id)
    add_list_entry_form = AddMailingListEntryForm(request.form)
    if add_list_entry_form.validate_on_submit():
        address = MailingAddressExtern(add_list_entry_form.address.data)
        db.session.add(address)
        db.session.commit()
        entry = MailingListEntry(lst.id, address.id)
        db.session.add(entry)
        db.session.commit()
        flash('Entry successfully added', 'success')
    return render_template('admin/mail/mailing_list.html', list=lst, add_list_entry_form=add_list_entry_form)
