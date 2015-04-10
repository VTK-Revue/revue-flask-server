__author__ = 'fkint'

from functools import wraps
from flask import redirect, flash

from revue.models import UserPermission, Permission
from revue.utilities import session


class Permissions:
    ADMIN = "admin"


def has_permission(user_id, permission_name):
    p = Permission.query.filter_by(name=permission_name).first()
    if p is None:
        return False
    up = UserPermission.query.filter_by(user=user_id, permission=p.id).first()
    if up is None:
        return False
    return True


# admin required decorator
def admin_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if not session.is_logged_in():
            flash('You need to login first.', 'danger')
            return redirect('/login')
        elif not has_permission(session.get_current_user_id(), Permissions.ADMIN):
            flash('You need to have admin permissions.', 'danger')
            return redirect('/')
        else:
            return f(*args, **kwargs)
    return wrap

