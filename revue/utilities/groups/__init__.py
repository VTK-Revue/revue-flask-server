__author__ = 'Floris'
from revue.models import GroupParticipation, User
from revue.models.menus import GroupMenu, MenuEntry


def get_group_members(group):
    return [User.query.get(group_participation.user) for group_participation in
            GroupParticipation.query.filter_by(group=group.id)]


def get_group_menu(group):
    group_menu = GroupMenu.query.get(group.id)
    if group_menu is None:
        return None
    return MenuEntry.query.get(group_menu.menu_entry_id)