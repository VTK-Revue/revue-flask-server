from revue import db, app
from revue.models.general import User, RevueYear
from revue.models.groups import PersistentGroupParticipation, Group, YearGroupParticipation, \
    YearParticipation, YearParticipationRequest, PersistentGroup, YearGroup, \
    SensitiveYearGroupParticipationRequest, SensitivePersistentGroupParticipationRequest
from revue.models.menus import GroupMenu, MenuEntry


# TODO: sanity checks and error messages (raise exceptions or return statuses?)

def get_group_by_id(id):
    return Group.query.get(id)


def get_group_by_name(name):
    return Group.query.filter_by(name=name).first()


def get_persistent_group_members(group):
    return [User.query.get(group_participation.user_id) for group_participation in
            PersistentGroupParticipation.query.filter_by(group_id=group.id)]


def get_year_group_members(year_group, revue_year):
    year_participations = filter(map(YearGroupParticipation.filter_by(year_group_id=year_group.id),
                                     lambda x: YearParticipation.query.get(x.year_participation_id)),
                                 lambda x: x.year_id == revue_year.id)
    return map(year_participations, lambda x: User.query.get(x.user_id))


def get_revue_year_by_year(year):
    return RevueYear.query.filter_by(year=year).first()


def get_revue_year_by_id(id):
    return RevueYear.query.get(id)


def request_year_participation(revue_year, user):
    p = YearParticipationRequest(revue_year.id, user.id)
    db.session.add(p)
    db.session.commit()


def get_year_groups():
    return YearGroup.query.all()


def join_year_group(year_group, revue_year, user):
    group = Group.query.filter_by(id=year_group.id).first()
    yp = get_year_participation(revue_year=revue_year, user=user)
    if group.sensitive:
        request = SensitiveYearGroupParticipationRequest(year_group.id, yp.id)
        db.session.add(request)
        db.session.commit()
        return False
    else:
        ygp = YearGroupParticipation(year_group_id=year_group.id, year_participation_id=yp.id)
        db.session.add(ygp)
        db.session.commit()
        return True


def join_persistent_group(persistent_group, user):
    group = Group.query.filter_by(id=persistent_group.id).first()
    if group.sensitive:
        request = SensitivePersistentGroupParticipationRequest(persistent_group.id, user.id)
        db.session.add(request)
        db.session.commit()
        return False
    else:
        group_participation = PersistentGroupParticipation(persistent_group_id=persistent_group.id, user_id=user.id)
        db.session.add(group_participation)
        db.session.commit()
        return True


def get_year_participation(revue_year, user):
    return YearParticipation.query.filter_by(year_id=revue_year.id, user_id=user.id).first()


def get_year_participation_request(revue_year, user):
    return YearParticipationRequest.query.filter_by(year_id=revue_year.id, user_id=user.id).first()


def get_year_group_participation(year_group, revue_year, user):
    year_participation = get_year_participation(revue_year, user)
    return YearGroupParticipation.query.filter_by(year_participation_id=year_participation.id,
                                                  year_group_id=year_group.id).first()


def leave_year_group(year_group, year, user):
    participation = get_year_group_participation(year_group, year, user)
    db.session.delete(participation)
    db.session.commit()


def get_persistent_group_participation(persistent_group, user):
    return PersistentGroupParticipation.query.filter_by(group_id=persistent_group.id, user_id=user.id).first()


# def get_specific_group_by_id(group_id):
#     # FIXME is it possible to do this automatically for all types of groups?
#     return PersistentGroup.query.filter_by(persistent_group_id=group_id) or \
#             YearGroup.query.filter_by(year_group_id=group_id)


def get_revue_year_members(revue_year):
    return [User.query.get(participation.user_id) for participation in
            YearParticipation.query.filter_by(year_id=revue_year.id)]


def leave_persistent_group(group, user):
    participation = get_persistent_group_participation(group, user)
    db.session.delete(participation)
    db.session.commit()


def get_group_menu(group):
    group_menu = GroupMenu.query.get(group.id)
    if group_menu is None:
        return None
    return MenuEntry.query.get(group_menu.menu_entry_id)


def get_user_persistent_groups(user):
    return [get_group_by_id(participation.group_id) for participation in
            PersistentGroupParticipation.query.filter_by(user_id=user.id)]


def get_user_year_participations(user):
    return YearParticipation.query.filter_by(user_id=user.id)


def get_user_year_group_participations_by_year_participation(year_participation):
    return YearGroupParticipation.query.filter_by(year_participation_id=year_participation.id)


def get_user_year_groups_by_year(user):
    result = dict()
    for year_participation in get_user_year_participations(user):
        revue_year = get_revue_year_by_id(year_participation.year_id)
        result[revue_year.year] = set()
        for year_group_participation in get_user_year_group_participations_by_year_participation(year_participation):
            result[revue_year.year].add(get_group_by_id(year_group_participation.year_group_id))
    return result


def get_all_revue_years():
    return RevueYear.query.all()


def get_year_participations(revue_year):
    return YearParticipation.query.filter_by(year_id=revue_year.id)


def get_year_participation_requests(revue_year):
    return YearParticipationRequest.query.filter_by(year_id=revue_year.id)


def approve_year_participation_request(user, revue_year):
    year_participation_request = get_year_participation_request(revue_year, user)
    year_participation = YearParticipation(revue_year.id, user.id)
    year_participation.id = year_participation_request.id
    year_participation.participation_id = year_participation_request.id
    db.session.delete(year_participation_request)
    db.session.commit()
    db.session.add(year_participation)
    db.session.commit()


def reject_year_participation_request(user, revue_year):
    year_participation_request = get_year_participation_request(revue_year, user)
    db.session.delete(year_participation_request)
    db.session.commit()


def get_pending_year_participation_requests(revue_year):
    return [x for x in get_year_participation_requests(revue_year) if
            get_year_participation(revue_year, x.user()) is None]


def get_year_group_members_by_year(year_group):
    return {revue_year.year: year_group.members(revue_year) for revue_year in get_all_revue_years()}


def get_current_year():
    return get_revue_year_by_year(int(app.config['CURRENT_YEAR']))


def get_sensitive_year_group_participation_requests():
    return SensitiveYearGroupParticipationRequest.query.all()


def get_sensitive_persistent_group_participation_requests():
    return SensitivePersistentGroupParticipationRequest.query.all()


def approve_sensitive_persistent_group_participation_request(user, group):
    request = SensitivePersistentGroupParticipationRequest(persistent_group_id=group.id, user_id=user.id)
    group_participation = PersistentGroupParticipation(persistent_group_id=persistent_group.id, user_id=user.id)
    db.session.delete(request)
    db.session.commit()
    db.session.add(group_participation)
    db.session.commit()


def approve_sensitive_year_group_participation_request(user, revue_year, year_group):
    year_participation = get_year_participation(revue_year=revue_year, user=user)
    request = SensitiveYearGroupParticipationRequest(year_group_id=year_group.id, year_participation_id=year_participation.id)
    ygp = YearGroupParticipation(year_group_id=year_group.id, year_participation_id=year_participation.id)
    db.session.delete(request)
    db.session.commit()
    db.session.add(ygp)
    db.session.commit()
