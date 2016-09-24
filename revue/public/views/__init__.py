from flask import render_template, Blueprint

public_site = Blueprint('public', __name__, template_folder='../templates')

from . import login


@public_site.route("/")
@public_site.route("/index")
@public_site.route("/home")
def index():
    return render_template("public/home.html")