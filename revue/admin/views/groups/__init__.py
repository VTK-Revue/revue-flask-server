from flask import render_template, request, flash, redirect, url_for

from revue import db
from revue.admin.views import admin_site
from revue.models.groups import PersistentGroup
from .forms import CreatePersistentGroupForm


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
