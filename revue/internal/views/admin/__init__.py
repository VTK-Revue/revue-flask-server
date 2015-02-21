@internal_site.route("/user")
@login_required
def user():
    return render_template("internal/admin/user.html")