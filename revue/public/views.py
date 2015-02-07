from flask import render_template, Blueprint, redirect, url_for, request, flash, session
from revue.login import login_required

public_site = Blueprint('public', __name__, template_folder='templates')

@public_site.route("/")
@public_site.route("/index")
def index():
    return render_template("public/index.html")

@public_site.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            flash('Invalid login', 'danger')
        else:
            session['logged_in'] = True
            flash('You just logged in', 'success')
            return redirect('intern')

    return render_template("public/login.html")

@public_site.route("/logout")
@login_required
def logout():
    session.pop('logged_in', None)
    flash('You just logged lout', 'success')
    return redirect('')

@public_site.route("/info")
def info():
    return render_template("public/info.html")

@public_site.route("/archive")
def archive():
    return render_template("public/archive.html")


