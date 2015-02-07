from flask import render_template, Blueprint

public_site = Blueprint('public', __name__, template_folder='templates')

@public_site.route("/")
@public_site.route("/index")
def index():
    return render_template("public/index.html")

@public_site.route("/login")
def login():
    return render_template("public/login.html")

@public_site.route("/info")
def info():
    return render_template("public/info.html")

@public_site.route("/archive")
def archive():
    return render_template("public/archive.html")
