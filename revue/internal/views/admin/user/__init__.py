__author__ = 'fkint'

from flask import render_template, request
from .....models.general import User
from ...user.forms import UpdateUserPasswordForm, UpdateUserInfoForm
from revue import bcrypt, db


def show_user(username):
    user = User.query.filter_by(username=username).first()

    password_form = UpdateUserPasswordForm(request.form)
    info_form = UpdateUserInfoForm(request.form)
    return render_template("internal/user/user_edit.html",
                           u=user, password_form=password_form,
                           info_form=info_form,
                           password_update_target_url="/intern/admin/user/"+username+"?action=update_password",
                           info_update_target_url="/intern/admin/user/"+username+"?action=update_info")

def show_user_update(username):
    action = request.args.get('action', '')
    user = User.query.filter_by(username=username).first()
    if action == "update_password":
        form = UpdateUserPasswordForm(request.form)
        if form.validate():
            h = bcrypt.generate_password_hash(form.password.data)
            user.password = h
            db.session.commit()
        return render_template("internal/user/user_edit.html",
                       u=user, password_form=form,
                       info_form=UpdateUserInfoForm(request.form),
                       password_update_target_url="/intern/admin/user/"+username+"?action=update_password",
                       info_update_target_url="/intern/admin/user/"+username+"?action=update_info")
    elif action == "update_info":
        form = UpdateUserInfoForm(request.form)
        if form.validate():
            user.email = form.email.data
            user.firstName = form.firstName.data
            user.lastName = form.lastName.data
            db.session.commit()
        return render_template("internal/user/user_edit.html",
                       u=user, password_form=UpdateUserPasswordForm(request.form),
                       info_form=form,
                       password_update_target_url="/intern/admin/user/"+username+"?action=update_password",
                       info_update_target_url="/intern/admin/user/"+username+"?action=update_info")
    return show_user(username)