from functools import wraps
from flask import redirect, flash

from .utilities import session


# login required decorator
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if session.is_logged_in():
            return f(*args, **kwargs)
        else:
            flash('You need to login first.', 'danger')
            return redirect('/login')
    return wrap
