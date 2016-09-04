from sqlalchemy import ForeignKey, PrimaryKeyConstraint

from revue import db
from revue.models.pages import Page


class YearGroupYearPage(Page):
    __tablename__ = "year_group_year_page"
    __table_args__ = (PrimaryKeyConstraint('year_group_id', 'year_id'), {"schema": "content"})

    year_group_id = db.Column("year_group_id", db.Integer, ForeignKey('general.year_group.id'),
                              nullable=False)
    year_id = db.Column("year_id", db.Integer, ForeignKey("general.revue_year.id"), nullable=False)
    page_id = db.Column("page_id", db.Integer, ForeignKey('content.page.id'), nullable=False)

    def __init__(self, year_group, revue_year):
        Page.__init__(self, "{} - {}".format(year_group.name, revue_year.year),
              "{}'s page for {}".format(year_group.name, revue_year.year))
        self.year_group_id = year_group.id
        self.year_id = revue_year.id
