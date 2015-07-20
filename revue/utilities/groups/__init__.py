__author__ = 'Floris'
from revue.models import GroupParticipation, User


def get_group_members(group):
    return [User.query.get(group_participation.user) for group_participation in
            GroupParticipation.query.filter_by(group=group.id)]
