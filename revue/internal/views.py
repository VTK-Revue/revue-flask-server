from flask import render_template

from . import internal_site


@internal_site.route("/")
@internal_site.route("/index")
def index():
    return render_template("layout.html")
