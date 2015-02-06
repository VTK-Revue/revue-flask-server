from flask import render_template

from . import public_site


@public_site.route("/")
@public_site.route("/index")
def index():
    return render_template("layout.html") + "PUBLIC"
