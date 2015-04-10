__author__ = 'fkint'

from wtforms import Form, StringField, PasswordField, SubmitField, HiddenField, TextAreaField, BooleanField
from wtforms.validators import InputRequired, EqualTo, Length, Email


class EditContentElementForm(Form):
    identifier = StringField("Identifier", validators=[InputRequired()])
    sticky = BooleanField("Sticky")
    title = StringField("Title", validators=[InputRequired()])
    submit = SubmitField("Save")


class EditTextElementForm(EditContentElementForm):
    content = TextAreaField("Content")