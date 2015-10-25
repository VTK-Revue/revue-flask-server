from flask import render_template, request, redirect, url_for, flash

from revue.models.general import User
from .forms import UpdateUserInfoForm
from revue import db
from revue.admin.views import admin_site


@admin_site.route('/user/<username>', methods=['GET', 'POST'])
def edit_user(username):
    u = User.query.filter_by(username=username).first()
    form = UpdateUserInfoForm(request.form, u)
    if request.method == 'POST' and form.validate():
        form.populate_obj(u)
        db.session.commit()
        flash('Successfully updated user ' + username, 'success')
        return redirect(url_for('.edit_user', username=username))
    return render_template("admin/user/user_edit.html", info_form=form)


@admin_site.route('/users')
def all_users():
    users = User.query.paginate(int(request.args.get('page', 1)), 20)
    return render_template("admin/user/all_users.html", users=users)
