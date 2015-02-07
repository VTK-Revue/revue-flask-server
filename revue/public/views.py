from flask import render_template, Blueprint, redirect, url_for, request, flash, session
from revue.login import login_required
from forms import LoginForm

public_site = Blueprint('public', __name__, template_folder='templates')

@public_site.route("/")
@public_site.route("/index")
def index():
    return render_template("public/index.html")

@public_site.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST':
        print "validate: "+str(form.validate())
        if form.validate():
            if form.username.data != 'admin' or form.password.data != 'admin':
                print "wrong login"
                flash('Invalid login', 'danger')
            else:
                print "login"
                session['logged_in'] = True
                flash('You just logged in', 'success')
                return redirect('intern')
        print form.username

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


