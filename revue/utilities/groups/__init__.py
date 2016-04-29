from revue.models.groups import PersistentGroupParticipation, Group, YearGroup, YearGroupParticipation
from revue.models.general import User, RevueYear
from revue.models.menus import GroupMenu, MenuEntry


def get_group_members(group):
    return [User.query.get(group_participation.user_id) for group_participation in
            PersistentGroupParticipation.query.filter_by(group_id=group.id)]


def get_group_menu(group):
    group_menu = GroupMenu.query.get(group.id)
    if group_menu is None:
        return None
    return MenuEntry.query.get(group_menu.menu_entry_id)


def is_user_member_of_persistent_group(group_id, user_id):
    return PersistentGroupParticipation.query.filter_by(group_id=group_id, user_id=user_id).count() != 0


def is_user_member_of_year_group(group_id, user_id, year_id):
    return YearGroupParticipation.query.filter_by(group_id=group_id, user_id=user_id, year_id=year_id).count() != 0


def get_user_persistent_groups(user):
    return [Group.query.get(p.group_id) for p in PersistentGroupParticipation.query.filter_by(user_id=user.id)]


def get_user_year_groups_by_year(user):
    result = {year.year: set() for year in RevueYear.query.all()}
    for participation in YearGroupParticipation.query.filter_by(user_id=user.id):
        result[RevueYear.query.get(participation.year_id).year].add(YearGroup.query.get(participation.group_id))
    return result


def get_year_group_members_by_year(year_group_id):
    result = {year.year: set() for year in RevueYear.query.all()}
    for participation in YearGroupParticipation.query.filter_by(group_id=year_group_id):
        result[RevueYear.query.get(participation.year_id).year].add(User.query.get(participation.user_id))
    return result
