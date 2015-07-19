__author__ = 'fkint'

from revue.models import YearGroupParticipation, Page, PageAccessRestriction, ContentElement
from revue.utilities import session
from revue import db


def user_meets_restriction(restriction, user_id):
    ygp = YearGroupParticipation.query.filter_by(year_group=restriction.year_group, year=restriction.revue_year,
                                                 user=user_id).first()
    if ygp is None:
        return False
    return True


def has_access_to_page(page, user_id):
    if not page.access_restricted:
        return True
    restrictions = PageAccessRestriction.query.filter_by(page=page.id).all()
    for restriction in restrictions:
        if user_meets_restriction(restriction, user_id):
            return True
    return False


def get_page_by_id(id):
    return Page.query.get(id)

def get_page_by_path(path):
    path_parts = path.split("/")
    current_page = None
    for p in path_parts:
        if p == "":
            continue
        parent_page_id = None
        if current_page is not None:
            parent_page_id = current_page.id
        current_page = Page.query.filter_by(url_identifier=p, parent_page=parent_page_id).first()
        if current_page is None:
            return None
    if has_access_to_page(current_page, session.get_current_user_id()):
        return current_page
    return None


def get_content_element_by_id(id):
    print(id)
    content_element = db.session.query(ContentElement).filter_by(id=id).first()
    print(content_element)
    return content_element


def get_content_elements(page):
    return [pce.content_element for pce in page.page_content_elements]


def create_page(page):
    db.session.add(page)
    db.session.commit()


def save_page(page):
    db.session.commit()