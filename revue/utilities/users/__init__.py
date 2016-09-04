from revue.models.general import User


def get_all_users():
    return User.query.filter(User.activated is not None)


def get_user_by_id(user_id):
    return User.query.get(user_id)
