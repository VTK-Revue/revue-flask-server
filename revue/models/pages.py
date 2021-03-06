import revue.utilities.users as users
from revue import db


class Page(db.Model):
    __tablename__ = 'page'
    __table_args__ = (db.UniqueConstraint('parent_page_id', 'url_identifier'), {'schema': 'content'})
    id = db.Column('id', db.Integer, primary_key=True, nullable=False)
    title = db.Column(db.String(50), nullable=False)
    parent_page_id = db.Column("parent_page_id", db.Integer, db.ForeignKey("content.page.id"), nullable=True)
    description = db.Column(db.Text, nullable=False)
    access_restricted = db.Column("access_restricted", db.Boolean, nullable=False)
    url_identifier = db.Column('url_identifier', db.String(50), nullable=False)

    page_content_elements = db.relationship("PageContentElement", backref="page")

    def __init__(self, title, description):
        self.title = title
        self.parent_page_id = None
        self.description = description
        self.access_restricted = False,
        self.url_identifier = ""


class PageAccessRestriction(db.Model):
    __tablename__ = "page_access_restriction"
    __table_args__ = (db.PrimaryKeyConstraint("page_id", "year_group_id", "revue_year_id"), {"schema": "content"})
    page_id = db.Column("page_id", db.Integer, db.ForeignKey("content.page.id"), nullable=False)
    year_group_id = db.Column("year_group_id", db.Integer, db.ForeignKey("general.year_group.id"), nullable=False)
    revue_year_id = db.Column("revue_year_id", db.Integer, db.ForeignKey("general.revue_year.id"), nullable=False)

    def __init__(self, page_id, year_group_id, revue_year_id):
        self.page_id = page_id
        self.year_group_id = year_group_id
        self.revue_year_id = revue_year_id


class ContentElement(db.Model):
    __tablename__ = "content_element"
    __table_args__ = {"schema": "content"}

    id = db.Column("id", db.Integer, primary_key=True, nullable=False)
    type = db.Column("type", db.Enum("text", "container", "vuedle", "announcement", name="content_element_types"),
                     nullable=False)
    sticky = db.Column("sticky", db.Boolean, nullable=False, default=False)
    title = db.Column('title', db.String(50), nullable=False, default="")
    identifier = db.Column("identifier", db.String(50), nullable=False, default=None)
    author_id = db.Column('author_id', db.Integer, db.ForeignKey('general.user.id'), nullable=False)

    page_content_elements = db.relationship("PageContentElement", backref="content_element")

    __mapper_args__ = {
        'polymorphic_on': type
    }

    def __init__(self, type, sticky, title, identifier, author_id):
        self.type = type
        self.sticky = sticky
        self.title = title
        self.identifier = identifier
        self.author_id = author_id

    def author(self):
        print("author id = {}".format(self.author_id))
        if self.author_id is None:
            return None
        return users.get_user_by_id(self.author_id)


class PageContentElement(db.Model):
    __tablename__ = "page_content_element"
    __table_args__ = (db.PrimaryKeyConstraint('content_element_id', 'page_id'), {"schema": "content"})

    content_element_id = db.Column("content_element_id", db.Integer, db.ForeignKey('content.content_element.id'),
                                   nullable=False)
    page_id = db.Column("page_id", db.Integer, db.ForeignKey('content.page.id'), nullable=False)
    order_index = db.Column("order_index", db.Integer, nullable=False, default=0)

    def __init__(self, content_element_id, page_id, order_index):
        self.content_element_id = content_element_id
        self.page_id = page_id
        self.order_index = order_index


class TextElement(ContentElement):
    __tablename__ = "text_element"
    __table_args__ = {"schema": "content"}

    text_element_id = db.Column("id", db.Integer, db.ForeignKey('content.content_element.id'), primary_key=True,
                                nullable=False)
    content = db.Column("content", db.Text, nullable=False)

    __mapper_args__ = {
        "polymorphic_identity": "text"
    }

    def __init__(self, content):
        self.content = content
