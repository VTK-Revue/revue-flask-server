from flask_wtf import Form
from wtforms.fields import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Email, Length, EqualTo

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
        validators=[InputRequired(), Length(min = 3, max = 20)]
    )
    password = PasswordField(
        'Password',
        validators=[InputRequired(), Length(min = 6, max = 25)]
    )
    password_repeat = PasswordField(
        'Repeat Password',
        validators=[InputRequired(), EqualTo('password', message = 'Passwords must match.') ]
    )
    firstName = StringField(
        'First Name',
        validators=[InputRequired(), Length(min = 2, max = 60)]
    )
    lastName = StringField(
        'Last Name',
        validators=[InputRequired(), Length(min = 2, max = 60)]
    )
    email = StringField(
        'Email',
        validators=[InputRequired(), Email(), Length(min = 3, max = 50)]
    )

    submit = SubmitField('Register')