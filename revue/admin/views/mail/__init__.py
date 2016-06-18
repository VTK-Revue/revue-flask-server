from flask import flash, request, render_template, redirect, url_for

from revue import db
from revue.admin.views import admin_site
from revue.admin.views.mail.forms import AddMailingListEntryForm, CreateMailingListForm, \
    AddMailingListMultipleEntriesForm
from revue.models.mail import PersistentGroupMailingList, YearGroupMailingList, MailingList, MailingListEntry, \
    MailingAddressExtern
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


@admin_site.route('/mail/list/<int:list_id>/batch_add', methods=['GET', 'POST'])
def view_mailing_list_batch_add(list_id):
    lst = MailingList.query.get(list_id)
    add_multiple_entries_form = AddMailingListMultipleEntriesForm(request.form)
    if add_multiple_entries_form.validate_on_submit():
        addresses_lines = add_multiple_entries_form.addresses.data.splitlines()
        for line in addresses_lines:
            email = line.strip()
            if len(email) == 0:
                continue
            address = MailingAddressExtern(line)
            db.session.add(address)
            db.session.commit()
            entry = MailingListEntry(lst.id, address.id)
            db.session.add(entry)
            db.session.commit()
        flash('Entries successfully added', 'success')
    return render_template('admin/mail/mailing_list.html', list=lst, add_list_entry_form=add_multiple_entries_form)


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


@admin_site.route('/mail/list/entry/<int:entry_id>')
def remove_mailing_list_entry(entry_id):
    entry = MailingListEntry.query.get(entry_id)
    db.session.delete(entry)
    db.session.commit()
    return redirect(url_for('.view_mailing_list', list_id=entry.list_id))
