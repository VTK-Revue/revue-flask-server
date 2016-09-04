from revue import db
from revue.models.groups_content import YearGroupYearPage


def get_year_group_year_page(year_group, revue_year):
    return YearGroupYearPage.query.filter_by(year_group_id=year_group.id, year_id=revue_year.id).first()


def create_year_group_year_page(year_group, revue_year):
    page = YearGroupYearPage(year_group=year_group, revue_year=revue_year)
    db.session.add(page)
    db.session.commit()


def get_or_create_year_group_year_page(year_group, revue_year):
    page = get_year_group_year_page(year_group, revue_year)
    if page is None:
        create_year_group_year_page(year_group, revue_year)
        page = get_year_group_year_page(year_group, revue_year)
    return page
