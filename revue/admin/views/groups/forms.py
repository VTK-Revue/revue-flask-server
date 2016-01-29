from flask_wtf import Form
from wtforms.fields import StringField, SubmitField, TextAreaField, SelectField
from wtforms.validators import InputRequired, ValidationError

from revue.models.groups import *


class ExistsOrNone(object):
    def __init__(self, model, message=None):
        self.model = model
        self.message = message
        if message is None:
            self.message = u'This is not a valid persistent group'

    def __call__(self, form, field):
        if field.data is not None and self.model.query.get(field.data).first() is not None:
            raise ValidationError(self.message)


class CreatePersistentGroupForm(Form):
    name = StringField(
        'Name',
        validators=[InputRequired()]
    )
    description = TextAreaField(
        'Description',
        validators=[]
    )
    parent_persistent_group_id = SelectField(
        'Parent Group',
    )
    submit = SubmitField('Save')

    def __init__(self, form):
        Form.__init__(self, form)
        choices = {g.id: g.name for g in PersistentGroup.query.all()}
        choices[None] = '-'
        self.parent_persistent_group_id.choices = [(x, choices[x]) for x in choices.keys()]


class EditPersistentGroupForm(CreatePersistentGroupForm):
    pass

class CreateYearGroupForm(Form):
    name = StringField(
        'Name',
        validators=[InputRequired()]
    )
    description = TextAreaField(
        'Description',
        validators=[]
    )
    parent_year_group_id = SelectField(
        'Parent Group',
    )
    submit = SubmitField('Save')

    def __init__(self, form):
        Form.__init__(self, form)
        choices = {g.id: g.name for g in YearGroup.query.all()}
        choices[None] = '-'
        self.parent_year_group_id.choices = [(x, choices[x]) for x in choices.keys()]

class EditYearGroupForm(CreateYearGroupForm):
    pass