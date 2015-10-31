from flask_wtf import Form
from wtforms.fields import StringField, SubmitField, TextAreaField, SelectField
from wtforms.validators import InputRequired, ValidationError

from revue.models.groups import PersistentGroup


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
        # choices=[(None, '-')] + [(g.id, g.name) for g in PersistentGroup.query.all()]
        choices={None: '-'}.update({g.id: g.name for g in PersistentGroup.query.all()})
    )
    submit = SubmitField('Save')


class EditPersistentGroupForm(CreatePersistentGroupForm):
    pass
