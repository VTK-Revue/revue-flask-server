from flask import request, render_template, flash, redirect

from revue import bcrypt, db
from revue.models.general import User
from revue.public.views.forms import LoginForm, RegisterForm
from revue.public.views import public_site
from revue.utilities import session
from revue.models.mail import MailingAddressExtern

@public_site.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User.query.filter(User.username == form.username.data).first()
        if user is not None and \
                bcrypt.check_password_hash(user.password,
                                           form.password.data):
            if user.activated is not None:
                print(user.activated)
                session.user_login(user)
                flash('You just logged in', 'success')
                return redirect('intern')
            else:
                flash('Your account has not been activated yet', 'danger')
        else:
            flash('Invalid login', 'danger')

    return render_template("public/login/login.html", form=form)


@public_site.route("/register", methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        if User.query.filter_by(username=form.username.data).first() is None:
            new_email = MailingAddressExtern(form.email.data)
            db.session.add(new_email)
            db.session.commit()
            new_user = User(
                form.firstName.data,
                form.lastName.data,
                new_email.id,
                form.username.data,
                form.password.data
            )
            db.session.add(new_user)
            db.session.commit()
            # TODO: send notification e-mail to activate this account
            flash('You just created an account. Once your account has been activated, you\''
                  'll be able to access the internal part of website.', 'success')
            return redirect('/')
        flash('A user with this username already exists, choose another one')
    return render_template("public/login/register.html", form=form)
