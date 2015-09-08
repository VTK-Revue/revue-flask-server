from wtforms import Form, StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, EqualTo, Length, Email


class UpdateUserInfoForm(Form):
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
        validators=[InputRequired(), Email(), Length(min=3, max=100)]
    )
    submit = SubmitField('Save')

    def set_user(self, user):
        # self.firstName.data
        self.firstName.default = user.firstName
        self.lastName.default = user.lastName
        self.email.default = user.email


class UpdateUserPasswordForm(Form):
    password = PasswordField(
        'Password',
        validators=[InputRequired(), Length(min=6, max=25)]
    )
    password_repeat = PasswordField(
        'Repeat Password',
        validators=[InputRequired(), EqualTo('password',
                                             message='Passwords must match.')]
    )
    submit = SubmitField("Update password")
