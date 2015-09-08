from flask import request, render_template, flash, redirect

from revue.public.views import public_site
from revue.public.views import LoginForm, RegisterForm
from revue.utilities import session
from revue.models import User, Registration
from revue import bcrypt, db


@public_site.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None and \
                bcrypt.check_password_hash(user.password,
                                           form.password.data):
            session.user_login(user)
            flash('You just logged in', 'success')
            return redirect('intern')
        else:
            flash('Invalid login', 'danger')

    return render_template("public/login/login.html", form=form)


@public_site.route("/register", methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        if User.query.filter_by(username=form.username.data).first() is None:
            newUser = User(
                form.firstName.data,
                form.lastName.data,
                form.email.data,
                form.username.data,
                form.password.data
            )
            # TODO: check if duplicate username should be checked
            db.session.add(Registration.from_user(newUser))
            db.session.commit()
            # TODO: send notification e-mail to activate this account
            flash('You just created an account. Once your account has been activated, you\''
                  'll be able to access the internal part of website.', 'success')
            return redirect('/')
        flash('A user with this username already exists, choose another one')
    return render_template("public/login/register.html", form=form)
