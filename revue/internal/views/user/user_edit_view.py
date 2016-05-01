from flask import render_template, request, flash, redirect, url_for

from . import internal_site
from .forms import UpdateUserPasswordForm, UpdateUserInfoForm
from revue import db, bcrypt
from revue.utilities import session


@internal_site.route("/profile", methods=["GET", "POST"])
def profile():
    user = session.get_current_user()
    info_form = UpdateUserInfoForm(request.form, user)
    if info_form.validate_on_submit():
        info_form.populate_obj(user)
        db.session.commit()
    return render_template("internal/user/user_edit.html", info_form=info_form)


@internal_site.route('/user/new_password', methods=["GET", "POST"])
def new_password():
    password_form = UpdateUserPasswordForm(request.form)
    if request.method == "POST" and password_form.validate():
        h = bcrypt.generate_password_hash(password_form.password.data)
        user = session.get_current_user()
        user.password = h.decode("utf-8")
        db.session.commit()
        flash('Password successfully updated', 'success')
        return redirect(url_for('.profile'))
    return render_template('internal/user/new_password.html', password_form=password_form)
