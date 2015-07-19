__author__ = 'fkint'

from wtforms import Form, StringField, PasswordField, SubmitField, HiddenField, TextAreaField, BooleanField
from wtforms.validators import InputRequired, EqualTo, Length, Email

class ContentElementForm(Form):
    identifier = StringField("Identifier", validators=[InputRequired()])
    sticky = BooleanField("Sticky")
    title = StringField("Title", validators=[InputRequired()])
    submit = SubmitField("Save")

class EditContentElementForm(ContentElementForm):
    pass

class CreateTextElementForm(ContentElementForm):
    content = TextAreaField("Content")



class EditTextElementForm(EditContentElementForm):
    content = TextAreaField("Content")

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