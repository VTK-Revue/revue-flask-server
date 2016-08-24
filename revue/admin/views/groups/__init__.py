from flask import render_template, request, flash, redirect, url_for

from revue.admin.views import admin_site
from revue.models.mail import PersistentGroupMailingList,YearGroupMailingList
from .forms import *
from revue.admin.views.groups import years

@admin_site.route('/groups', methods=['GET'])
def group_page():
    groups = Group.query.paginate(1, per_page=20, error_out=False)
    return render_template('admin/groups/group_page.html', groups=groups)


@admin_site.route('/persistent_groups/create', methods=['POST', 'GET'])
def create_persistent_group():
    form = CreatePersistentGroupForm(request.form)
    if form.validate_on_submit():
        pg = PersistentGroup()
        form.populate_obj(pg)
        db.session.add(pg)
        db.session.commit()
        flash('Successfully created persistent group ' + pg.name, 'success')
        return redirect(url_for('.edit_persistent_group', id=pg.id))
    return render_template('admin/groups/create_persistent_group.html', form=form)


@admin_site.route('/persistent_groups')
def all_persistent_groups():
    groups = PersistentGroup.query.all()
    return render_template('admin/groups/all_persistent_groups.html', groups=groups)


@admin_site.route('/persistent_group/<int:id>/edit', methods=['POST', 'GET'])
def edit_persistent_group(id):
    pg = PersistentGroup.query.get(id)
    form = EditPersistentGroupForm(request.form, pg)
    pg_list = pg.mailing_list()
    generate_mailing_list_form = GenerateGroupMailingListForm(request.form, pg_list)
    if generate_mailing_list_form.validate_on_submit():
        pg_list = PersistentGroupMailingList(pg.id, generate_mailing_list_form.name.data)
        db.session.add(pg_list)
        db.session.commit()
        flash('Successfully added mailing list to persistent group', 'succes')
    if form.validate_on_submit():
        form.populate_obj(pg)
        db.session.commit()
        flash('Successfully edited persistent group', 'success')
    return render_template('admin/groups/edit_persistent_group.html', form=form, group=pg,
                           generate_mailing_list_form=generate_mailing_list_form)


@admin_site.route('/year_groups/create', methods=['POST', 'GET'])
def create_year_group():
    form = CreateYearGroupForm(request.form)
    if request.method == 'POST' and form.validate():
        yg = YearGroup()
        form.populate_obj(yg)
        db.session.add(yg)
        db.session.commit()
        flash('Successfully created year group ' + yg.name, 'success')
        return redirect(url_for('.edit_year_group', id=yg.id))
    return render_template('admin/groups/create_year_group.html', form=form)


@admin_site.route('/year_groups')
def all_year_groups():
    groups = YearGroup.query.all()
    return render_template('admin/groups/all_year_groups.html', groups=groups)


@admin_site.route('/year_group/<int:id>/edit', methods=['GET', 'POST'])
def edit_year_group(id):
    group = YearGroup.query.get(id)
    form = EditYearGroupForm(request.form, group)
    group_list = group.mailing_list()
    generate_mailing_list_form = GenerateGroupMailingListForm(request.form, group_list)
    if form.validate_on_submit():
        form.populate_obj(group)
        db.session.commit()
        flash('Successfully edited persistent group', 'success')
    if generate_mailing_list_form.validate_on_submit():
        group_list = YearGroupMailingList(group.id, generate_mailing_list_form.name.data)
        db.session.add(group_list)
        db.session.commit()
        flash('Successfully added mailing list to year group', 'succes')
    return render_template('admin/groups/edit_year_group.html', form=form, group=group,
                           generate_mailing_list_form=generate_mailing_list_form)


@admin_site.route('/group/<int:id>/edit', methods=['GET', 'POST'])
def edit_group(id):
    group = Group.query.get(id)
    if isinstance(group, YearGroup):
        return edit_year_group(id)
    elif isinstance(group, PersistentGroup):
        return edit_persistent_group(id)
    return 404
