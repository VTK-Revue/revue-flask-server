from wtforms import StringField, SubmitField, TextAreaField, BooleanField
from wtforms.validators import InputRequired
from revue.utilities.ui.forms import CKTextAreaField
from flask.ext.wtf import Form


class ContentElementForm(Form):
    identifier = StringField("Identifier", validators=[InputRequired()])
    sticky = BooleanField("Sticky")
    title = StringField("Title", validators=[InputRequired()])
    submit = SubmitField("Save")


class EditContentElementForm(ContentElementForm):
    pass


class CreateTextElementForm(ContentElementForm):
    content = CKTextAreaField("Content")


class EditTextElementForm(EditContentElementForm):
    content = CKTextAreaField("Content")


class PageForm(Form):
    url_identifier = StringField("Path", validators=[InputRequired()])
    title = StringField("Title", validators=[InputRequired()])
    description = TextAreaField("Description", validators=[InputRequired()])
    access_restricted = BooleanField('Access Restricted', validators=[])
    submit = SubmitField("Save")


class CreatePageForm(PageForm):
    pass


class EditPageForm(PageForm):
    pass
