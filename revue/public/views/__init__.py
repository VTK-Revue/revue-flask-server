from flask import render_template, Blueprint

from .forms import LoginForm, RegisterForm

public_site = Blueprint('public', __name__, template_folder='../templates')

from . import login


@public_site.route("/")
@public_site.route("/index")
@public_site.route("/home")
def index():
    return render_template("public/home.html")


@public_site.route("/ticket_info")
def ticket_info():
    return render_template("public/ticket_info.html")


@public_site.route("/contact")
def contact():
    return render_template("public/contact.html")


@public_site.route("/voorstellingen")
def voorstellingen():
    return render_template("public/voorstellingen.html")
