from wtforms.validators import ValidationError


class Unique(object):
    def __init__(self, model, field, message=None):
        self.model = model
        self.field = field
        self.message = message
        if message is None:
            self.message = u'This element already exists'

    def __call__(self, form, field):
        check = self.model.query.filter(self.field == field.data).first()
        if check:
            raise ValidationError(self.message)