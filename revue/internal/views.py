from flask import render_template, Blueprint

internal_site = Blueprint('intern', __name__, template_folder='templates')


@internal_site.route("/")
@internal_site.route("/index")
def index():
    return render_template("internal/index.html")

@internal_site.route("/logout")
def logout():
    return render_template("internal/logout.html")

@internal_site.route("/script")
def script():
    return render_template("internal/script.html")

@internal_site.route("/activities")
def activities():
    return render_template("internal/activities.html")
