from flask import render_template, request, flash, redirect, url_for

from revue import db
from revue.admin.views import admin_site
from revue.models.groups import *
from .forms import *

@admin_site.route('/groups', methods=['GET'])
def group_page():
    groups = Group.query.paginate(1,per_page=20,error_out=False)
    return render_template('admin/groups/group_page.html',groups=groups)


@admin_site.route('/persistent_groups/create', methods=['POST', 'GET'])
def create_persistent_group():
    form = CreatePersistentGroupForm(request.form)
    print(form.parent_persistent_group_id.choices)
    if request.method == 'POST' and form.validate():
        pg = PersistentGroup()
        form.populate_obj(pg)
        db.session.commit()
        flash('Successfully created persistent group ' + pg.name, 'success')
        return redirect(url_for('.edit_persistent_group', id=pg.id))
    return render_template('admin/groups/create_persistent_group.html', form=form)


@admin_site.route('/persistent_groups')
def all_persistent_groups():
    groups = PersistentGroup.query.all()
    return render_template('admin/groups/all_persistent_groups.html', groups=groups)


@admin_site.route('/persistent_group/<int:id>/edit')
def edit_persistent_group(id):
    group = PersistentGroup.get(id)
    return render_template('admin/groups/edit_persistent_group.html', group=group)

@admin_site.route('/year_groups/create', methods=['POST', 'GET'])
def create_year_group():
    form = CreateYearGroupForm(request.form)
    print(form.parent_year_group_id.choices)
    if request.method == 'POST' and form.validate():
        yg = YearGroup()
        form.populate_obj(yg)
        db.session.commit()
        flash('Successfully created year group ' + yg.name, 'success')
        return redirect(url_for('.edit_year_group', id=yg.id))
    return render_template('admin/groups/create_year_group.html', form=form)


@admin_site.route('/year_groups')
def all_year_groups():
    groups = YearGroup.query.all()
    return render_template('admin/groups/all_year_groups.html', groups=groups)


@admin_site.route('/year_group/<int:id>/edit')
def edit_year_group(id):
    group = YearGroup.get(id)
    return render_template('admin/groups/edit_year_group.html', group=group)