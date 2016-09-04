from revue.models.general import User


def get_all_users():
    return User.query.filter(User.activated is not None)
