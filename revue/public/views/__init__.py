from flask import render_template, Blueprint, redirect, url_for, request, \
    flash, session
from revue.login import login_required
from forms import LoginForm, RegisterForm
from revue.models import User, Registration
from revue import db, bcrypt

public_site = Blueprint('public', __name__, template_folder='../templates')


@public_site.route("/")
@public_site.route("/index")
def index():
    return render_template("public/index.html")


@public_site.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
            user = User.query.filter_by(username=form.username.data).first()
            if user is not None and \
                    bcrypt.check_password_hash(user.password,
                                               form.password.data):
                session['logged_in'] = True
                session['logged_in_user_id'] = user.id
                flash('You just logged in', 'success')
                return redirect('intern')
            else:
                flash('Invalid login', 'danger')

    return render_template("public/login.html", form=form)


@public_site.route("/logout")
@login_required
def logout():
    session.pop('logged_in', None)
    flash('You just logged out', 'success')
    return redirect('')


@public_site.route("/info")
def info():
    return render_template("public/info.html")


@public_site.route("/archive")
def archive():
    return render_template("public/archive.html")


@public_site.route("/register", methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        newUser = User(
            form.firstName.data,
            form.lastName.data,
            form.email.data,
            form.username.data,
            form.password.data
        )
        db.session.add(Registration.from_user(newUser))
        db.session.commit()
        #TODO: send notification e-mail to activate this account
        flash('You just created an account. Once your account has been activated, you\''
              'll be able to access the internal part of website.', 'success')
        return redirect('/')
    return render_template("public/register.html", form=form)
