__author__ = 'fkint'

from functools import wraps
from flask import session, redirect, flash

from revue.login import login_required

class Permissions:
    ADMIN = "admin"



def has_permission(user_id, permission_id):
    print("has permission check")
    if permission_id is None:
        return False
    return True


# admin required decorator
def admin_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' not in session:
            flash('You need to login first.', 'danger')
            return redirect('/login')
        elif not has_permission(session['logged_in_user_id'], Permissions.ADMIN):
            flash('You need to have admin permissions.', 'danger')
            return redirect('/')
        else:
            return f(*args, **kwargs)
    return wrap

