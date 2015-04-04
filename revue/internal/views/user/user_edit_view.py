__author__ = 'fkint'
from flask import render_template, session, request, url_for, flash

from .forms import UpdateUserPasswordForm, UpdateUserInfoForm
from ....models import User
from revue import db, bcrypt


def show():
    user = User.query.filter_by(id=session['logged_in_user_id']).first()

    password_form = UpdateUserPasswordForm(request.form)
    info_form = UpdateUserInfoForm(request.form)
    return render_template("internal/user/user_edit.html",
                           u=user, password_form=password_form,
                           info_form=info_form,
                           password_update_target_url="/intern/user?action=update_password",
                           info_update_target_url="/intern/user?action=update_info")


def show_update():
    action = request.args.get('action', '')
    user = User.query.filter_by(id=session['logged_in_user_id']).first()
    if action == "update_password":
        form = UpdateUserPasswordForm(request.form)
        if form.validate():
            h = bcrypt.generate_password_hash(form.password.data)
            user.password = h
            db.session.commit()
        return render_template("internal/user/user_edit.html",
                       u=user, password_form=form,
                       info_form=UpdateUserInfoForm(request.form),
                       password_update_target_url="/intern/user?action=update_password",
                       info_update_target_url="/intern/user?action=update_info")
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
                       password_update_target_url="/intern/user?action=update_password",
                       info_update_target_url="/intern/user?action=update_info")
    return show()
