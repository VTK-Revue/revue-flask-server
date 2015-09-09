from revue.models.groups import GroupParticipation, Group, YearGroup, YearGroupParticipation, RevueYear
from revue.models.general import User
from revue.models.menus import GroupMenu, MenuEntry


def get_group_members(group):
    return [User.query.get(group_participation.user) for group_participation in
            GroupParticipation.query.filter_by(group=group.id)]


def get_group_menu(group):
    group_menu = GroupMenu.query.get(group.id)
    if group_menu is None:
        return None
    return MenuEntry.query.get(group_menu.menu_entry_id)


def get_user_groups(user):
    return [Group.query.get(p.group) for p in GroupParticipation.query.filter_by(user=user.id)]


def get_user_year_groups_by_year(user):
    result = {year.year: set() for year in RevueYear.query.all()}
    for participation in YearGroupParticipation.query.filter_by(user=user.id):
        result[RevueYear.query.get(participation.year).year].add(YearGroup.query.get(participation.year_group))
    return result
