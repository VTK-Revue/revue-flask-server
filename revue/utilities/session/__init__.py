from flask import session

from revue.models.general import User


def is_logged_in():
    return 'logged_in' in session


def get_current_user_id():
    return session['logged_in_user_id']


def get_current_user():
    print(get_current_user_id())
    return User.query.filter_by(id=get_current_user_id()).first()


def user_login(user):
    session['logged_in'] = True
    session['logged_in_user_id'] = user.id


def user_logout():
    session.pop('logged_in', None)
    session.pop('logged_in_user_id', None)
