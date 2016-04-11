from flask_wtf import Form
from wtforms.fields import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Email, Length, EqualTo, ValidationError

from revue.models.general import User


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


class LoginForm(Form):
    username = StringField(
        'Username',
        validators=[InputRequired()]
    )
    password = PasswordField(
        'Password',
        validators=[InputRequired()]
    )
    submit = SubmitField('Login')


class RegisterForm(Form):
    username = StringField(
        'Username',
        validators=[InputRequired(),
                    Length(min=3, max=20),
                    Unique(User, User.username, "A user with this username already exists.")]
    )
    password = PasswordField(
        'Password',
        validators=[InputRequired(), Length(min=6, max=25)]
    )
    password_repeat = PasswordField(
        'Repeat Password',
        validators=[InputRequired(), EqualTo('password',
                                             message='Passwords must match.')]
    )
    firstName = StringField(
        'First Name',
        validators=[InputRequired(), Length(min=2, max=60)]
    )
    lastName = StringField(
        'Last Name',
        validators=[InputRequired(), Length(min=2, max=60)]
    )
    email = StringField(
        'Email',
        validators=[InputRequired(), Email(), Length(min=3, max=50)]
    )

    submit = SubmitField('Register')
